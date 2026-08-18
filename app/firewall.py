import uuid
from datetime import datetime
from app.models import PermissionRequest, PermissionDecision


class PermissionFirewall:

    def __init__(self):
        self.allowed_actions = {
            "read_file",
            "database_query",
            "send_email",
            "delete_file",
            "delete_database",
            "modify_permissions",
        }

        self.high_risk_actions = {
            "delete_file",
            "delete_database",
            "modify_permissions",
        }

        self.pending_approvals = {}
        self.audit_logs = []  # Complete history of access decisions

    def _log_event(self, agent_id: str, action: str, resource: str, decision: str, reason: str):
        self.audit_logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "resource": resource,
            "decision": decision,
            "reason": reason,
        })

    def check_permission(self, request: PermissionRequest) -> PermissionDecision:
        # 1. Block unregistered actions
        if request.action not in self.allowed_actions:
            reason = f"Action '{request.action}' is not permitted by system policy."
            self._log_event(request.agent_id, request.action, request.resource, "DENIED", reason)
            return PermissionDecision(allowed=False, reason=reason, expires_in=0)

        # 2. Check for existing admin approval
        for approval_id, data in self.pending_approvals.items():
            if (
                data["request"].agent_id == request.agent_id
                and data["request"].action == request.action
                and data["status"] == "APPROVED"
            ):
                reason = f"Action permitted via Admin Approval (ID: {approval_id})."
                self._log_event(request.agent_id, request.action, request.resource, "ALLOWED", reason)
                return PermissionDecision(
                    allowed=True,
                    reason=reason,
                    expires_in=request.duration_seconds,
                )

        # 3. Flag high-risk actions
        if request.action in self.high_risk_actions:
            approval_id = str(uuid.uuid4())[:8]
            self.pending_approvals[approval_id] = {
                "request": request,
                "status": "PENDING",
            }
            reason = f"HIGH RISK: Action '{request.action}' requires human approval. Approval ID: {approval_id}"
            self._log_event(request.agent_id, request.action, request.resource, "PENDING_APPROVAL", reason)
            return PermissionDecision(allowed=False, reason=reason, expires_in=0)

        # 4. Allow standard low-risk actions
        reason = "Action permitted."
        self._log_event(request.agent_id, request.action, request.resource, "ALLOWED", reason)
        return PermissionDecision(
            allowed=True,
            reason=reason,
            expires_in=request.duration_seconds,
        )