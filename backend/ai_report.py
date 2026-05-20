import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schemas import AnalysisResponse, AIReportResponse

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_report(analysis: AnalysisResponse) -> AIReportResponse:
    prompt = f"""
You are an incident response assistant.

Using the structured incident analysis below, write an operational report.

Analysis:
{analysis.model_dump_json(indent=2)}

Return only valid JSON with these keys:
executiveSummary, technicalSummary, likelyRootCause, recommendedActions.
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )

    text = response.output_text
    data = json.loads(text)

    return AIReportResponse(**data)