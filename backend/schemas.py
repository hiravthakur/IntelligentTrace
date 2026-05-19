from pydantic import BaseModel
from typing import Optional, List


class LogEvent(BaseModel):
    timestamp: Optional[str]
    service: Optional[str]
    severity: str
    message: str
    raw: str


class ParseResponse(BaseModel):
    eventCount: int
    services: List[str]
    events: List[str]
