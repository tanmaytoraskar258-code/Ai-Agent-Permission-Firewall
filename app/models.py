from pydantic import BaseModel, Field
from typing import Literal


class PermissionRequest(BaseModel):
    agent_id: str
    action: str
    resource: str
    reason: str
    risk_level: Literal["low", "medium", "high"] = "low"
    duration_seconds: int = Field(default=60, gt=0, le=3600)


class PermissionDecision(BaseModel):
    allowed: bool
    reason: str
    expires_in: int