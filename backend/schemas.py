from pydantic import BaseModel
from typing import Optional, List, Dict


class LogEvent(BaseModel):
    timestamp: Optional[str]
    service: Optional[str]
    severity: str
    message: str
    raw: str

class DependencyEdge(BaseModel):
    source: str
    target: str


class ParseResponse(BaseModel):
    eventCount: int
    services: List[str]
    events: List[LogEvent]

class TimeLineItem(BaseModel):
    timestamp: str
    severity: str
    service: str
    message: str

class AnalysisResponse(BaseModel):
    totalEvents: int
    errorCount: int
    warnCount: int
    infoCount: int
    services: List[str]
    serviceCounts: Dict[str, int]
    mostAffectedService: Optional[str]
    rootCause: str
    timeline: List[TimeLineItem]
    recommendations: List[str]
    dependencies: List[DependencyEdge]
    cascadeDetected: bool

class SummaryResponse(BaseModel):
    totalEvents: int
    errorCount: int
    warnCount: int
    infoCount: int
    services: List[str]
    serviceCounts: Dict[str, int]
    mostAffectedService: Optional[str]
