from fastapi import FastAPI, UploadFile, File
from schemas import ParseResponse, AnalysisResponse, SummaryResponse, AIReportResponse
from parser import parseLog
from analyzer import analyzeEvents, summarizeEvents
from fastapi.middleware.cors import CORSMiddleware
from ai_report import generate_ai_report

app = FastAPI(title = "IntelligentTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/ai-report", response_model=AIReportResponse)
async def aiReportFile(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    events = parseLog(text)
    analysis = analyzeEvents(events)

    return generate_ai_report(analysis)

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
