from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models import PermissionRequest, PermissionDecision
from app.firewall import PermissionFirewall
from app.tools import execute_tool

app = FastAPI(
    title="AI Agent Permission Firewall",
    description="A security firewall layer intercepting AI agent actions.",
    version="0.1.0"
)

firewall = PermissionFirewall()


class ToolExecutionRequest(BaseModel):
    agent_id: str
    action: str
    resource: str
    reason: str


@app.get("/")
def home():
    return {"message": "AI Agent Permission Firewall is active."}


@app.post("/check-permission", response_model=PermissionDecision)
def check_permission(request: PermissionRequest):
    return firewall.check_permission(request)


@app.post("/approve/{approval_id}")
def approve_request(approval_id: str):
    if approval_id not in firewall.pending_approvals:
        raise HTTPException(status_code=404, detail="Approval ID not found or already processed.")
    
    firewall.pending_approvals[approval_id]["status"] = "APPROVED"
    req_data = firewall.pending_approvals[approval_id]["request"]
    
    return {
        "status": "SUCCESS",
        "approval_id": approval_id,
        "message": f"Action '{req_data.action}' requested by '{req_data.agent_id}' has been APPROVED by admin."
    }


@app.post("/execute-tool")
def run_tool(request: ToolExecutionRequest):
    return execute_tool(
        firewall_instance=firewall,
        agent_id=request.agent_id,
        action=request.action,
        resource=request.resource,
        reason=request.reason
    )


@app.get("/audit-logs")
def get_audit_logs():
    return {
        "total_logs": len(firewall.audit_logs),
        "logs": firewall.audit_logs
    }