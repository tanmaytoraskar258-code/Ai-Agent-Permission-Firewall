from app.models import PermissionRequest

def execute_tool(firewall_instance, agent_id: str, action: str, resource: str, reason: str):
    """
    Wrapper function that routes tool execution through a shared firewall instance.
    """
    request = PermissionRequest(
        agent_id=agent_id,
        action=action,
        resource=resource,
        reason=reason,
        risk_level="high" if action in firewall_instance.high_risk_actions else "low",
        duration_seconds=60,
    )

    decision = firewall_instance.check_permission(request)

    if not decision.allowed:
        return {
            "status": "BLOCKED",
            "firewall_reason": decision.reason,
            "output": None,
        }

    # Execute actual tool if allowed
    if action == "read_file":
        output = f"Reading file: {resource}"
    elif action == "database_query":
        output = f"Executing database query on: {resource}"
    elif action == "send_email":
        output = f"Email sent regarding: {resource}"
    elif action == "delete_file":
        output = f"⚠️ File deleted: {resource}"
    elif action == "delete_database":
        output = f"⚠️ Database deleted: {resource}"
    elif action == "modify_permissions":
        output = f"⚠️ Permissions modified for: {resource}"
    else:
        output = f"Executed generic tool: {action}"

    return {
        "status": "EXECUTED",
        "firewall_reason": decision.reason,
        "output": output,
    }