import re
from typing import List, Optional

from schemas import LogEvent

SEVERITY_KEYWORDS = {
    "ERROR": ["error", "failed", "failure", "crashed", "timeout", "exception"],
    "WARN": ["warn", "warning", "retry", "slow", "latency", "degraded"],
    "INFO": ["info", "started", "completed", "success", "connected"],
}

def detectSeverity(input: str) -> str:
    lower = input.lower()
    upper = input.upper()

    if "ERROR" in upper:
        return "ERROR"
    
    if "WARN" in upper:
        return "WARN"
    
    if "WARNING" in upper:
        return "WARN"
    
    if "INFO" in upper:
        return "INFO"

    for severity, keywords in SEVERITY_KEYWORDS.items():
        if any(x in lower for x in keywords):
            return severity
    
    return "INFO"

def extractTimestamp(input: str) -> Optional[str]:
    patterns = [
        r"\d{2}:\d{2}:\d{2}",
        r"\d{2}:\d{2}",
        r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}",
    ]

    for x in patterns:
        match = re.search(x, input)
        
        if match:
            return match.group(0)
    
    return None

def extractService(input: str) -> Optional[str]:
    patterns = [
          r"\[(.*?)\]",
        r"service=([a-zA-Z0-9_-]+)",
        r"([a-zA-Z0-9_-]+-service)",
        r"([a-zA-Z0-9_-]+-worker)",
        r"([a-zA-Z0-9_-]+-api)",
        r"(database|db|redis|queue|gateway)",
    ]

    for x in patterns:
        match = re.search(x, input, re.IGNORECASE)

        if match:
            return match.group(1)
        
        return None
    
def parseLog(input: str) -> List[LogEvent]:

    events = []

    for x in input.splitlines():
        x = x.strip()

        if not x:
            continue

        event = LogEvent(
            timestamp = extractTimestamp(x),
            severity = detectSeverity(x),
            service = extractService(x),
            message = x,
            raw = x )
        
        events.append(event)
    
    return events