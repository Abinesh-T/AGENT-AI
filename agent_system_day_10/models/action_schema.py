from pydantic import BaseModel
from typing import Dict, Any


class AgentAction(BaseModel):
    tool: str
    parameters: Dict[str, Any]