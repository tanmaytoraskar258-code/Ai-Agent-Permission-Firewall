from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Agent Permission Firewall is active."}


def test_execute_allowed_tool():
    payload = {
        "agent_id": "test-agent",
        "action": "read_file",
        "resource": "config.json",
        "reason": "Reading config"
    }
    response = client.post("/execute-tool", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "EXECUTED"
    assert "Reading file" in data["output"]


def test_execute_blocked_tool():
    payload = {
        "agent_id": "test-agent",
        "action": "delete_database",
        "resource": "prod_db",
        "reason": "Testing wipe"
    }
    response = client.post("/execute-tool", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"
    assert data["output"] is None
    assert "HIGH RISK" in data["firewall_reason"]


def test_audit_logs():
    response = client.get("/audit-logs")
    assert response.status_code == 200
    data = response.json()
    assert "total_logs" in data
    assert isinstance(data["logs"], list)