from typing import List, Dict, Optional
from schemas import LogEvent, AnalysisResponse, SummaryResponse

def countBySeverity(events: List[LogEvent], severity: str) -> int:
    temp = 0

    for event in events:
        if event.severity == severity:
            temp += 1

    return temp

def getServiceCount(events: List[LogEvent]) -> Dict[str, int]:
    serviceCounts = {}

    for event in events:
        if event.service is None:
            continue
        
        if event.service not in serviceCounts:

            serviceCounts[event.service] = 0
        serviceCounts[event.service] += 1

    return serviceCounts

def getMostAffected(serviceCounts: Dict[str, int]) -> Optional[str]:
    if not serviceCounts:
        return None
    
    return max(serviceCounts, key = serviceCounts.get)

def buildTimeline(events: List[LogEvent]) -> List[str]:
    timeline = []

    for x in events:
        if x.severity in ["ERROR", "WARN"]:
           timestamp = x.timestamp or 'Unknown Time'

           service = x.service or 'Unknown Service'

           timeline.append(f"{timestamp} ||| {x.severity} ||| {service} ||| {x.message}")
    
    return timeline

#generic function to provide root cause, can be expanded later with more complex logic or ML models
def guessCause(events: List[LogEvent]) -> str:
    errorMessages = [
        event.message.lower()
        for event in events
        if event.severity == "ERROR"
    ]

    all_errors = " ".join(errorMessages)

    if "database" in all_errors or "db" in all_errors or "connection timeout" in all_errors:
        return (
            "Likely database connectivity or availability issue. "
            "Database-related errors appear before downstream service failures."
        )

    if "gateway" in all_errors or "502" in all_errors or "503" in all_errors:
        return (
            "Likely gateway or upstream routing issue. "
            "Gateway failures suggest requests could not be completed successfully."
        )

    if "worker" in all_errors or "crashed" in all_errors:
        return (
            "Likely worker process instability. "
            "Worker crashes appear in the incident log."
        )

    if len(errorMessages) > 0:
        return (
            "Errors were detected, but the likely root cause is unclear from current logs."
        )

    return "No critical root cause detected. Logs do not contain ERROR-level events."

#generic reccomendations for remediation, can be expanded later with more complex logic or ML models
def recommendations(events: List[LogEvent]) -> List[str]:
    recs = []

    messages = " ".join(event.message.lower() for event in events)

    if "timeout" in messages or "database" in messages or "db" in messages:
        recs.append("Check database health, connection pool limits, and query latency.")

    if "gateway" in messages or "502" in messages or "503" in messages:
        recs.append("Inspect gateway routing, upstream service health, and recent deployment changes.")

    if "worker" in messages or "crashed" in messages:
        recs.append("Review worker logs, restart history, memory usage, and exception traces.")

    if "retry" in messages or "queue" in messages:
        recs.append("Inspect retry queue depth, dead-letter queues, and backlog recovery behavior.")

    if not recs:
        recs.append("No specific remediation found. Review logs around WARN and ERROR events.")

    return recs

def analyzeEvents(events: List[LogEvent]) -> AnalysisResponse:
    summary = summarizeEvents(events)

    return AnalysisResponse(
        totalEvents=summary.totalEvents,
        errorCount=summary.errorCount,
        warnCount=summary.warnCount,
        infoCount=summary.infoCount,
        services=summary.services,
        serviceCounts=summary.serviceCounts,
        mostAffectedService=summary.mostAffectedService,
        rootCause = guessCause(events),
        timeline=buildTimeline(events),
        recommendations=recommendations(events),
    )

def summarizeEvents(events: List[LogEvent]) -> SummaryResponse:
    service_counts = getServiceCount(events)
    services = sorted(service_counts.keys())

    return SummaryResponse(
        totalEvents = len(events),
        errorCount = countBySeverity(events, "ERROR"),
        warnCount = countBySeverity(events, "WARN"),
        infoCount = countBySeverity(events, "INFO"),
        services = services,
        serviceCounts = service_counts,
        mostAffectedService = getMostAffected(service_counts),
    )