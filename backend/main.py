from fastapi import FastAPI, UploadFile, File
from schemas import ParseResponse, AnalysisResponse, SummaryResponse
from parser import parseLog
from analyzer import analyzeEvents, summarizeEvents

app = FastAPI(title = "IntelligentTrace API")

@app.get("/")

def root():
    return {"message": "Backend is working"}

@app.post("/parse", response_model = ParseResponse)

@app.post("/analyze", response_model = AnalysisResponse)
async def analyzeFile(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors = "ignore")

    events = parseLog(text)

    return analyzeEvents(events)

@app.post("/summary", response_model= SummaryResponse)
async def summarizeFile(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors = "ignore")

    events = parseLog(text)

    return summarizeEvents(events)

async def parseFile(file: UploadFile = File(...)):
    content = await file.read()

    text = content.decode("utf-8", errors = "ignore")

    events = parseLog(text)

    services = sorted(
        list({event.service for event in events if event.service is not None})
    )

    return ParseResponse(
        eventCount = len(events),
        services = services,
        events = events
    )
