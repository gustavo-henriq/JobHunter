from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import google.genai as genai
from user_profile import build_profile_prompt
from database import get_silver_jobs, upsert_gold_job

load_dotenv()


class JobScore(BaseModel):
    score: int = Field(description="0 to 5 match score")
    opportunity_type: str = Field(description="Example: estágio, vaga júnior, trainee")
    area: str = Field(description="Main professional area")
    focus: str = Field(description="Main work focus")
    tools: list[str] = Field(description="Main technologies, tools, or skills")


def get_client():
    AI_API_KEY = os.getenv("AI_API_KEY")
    return genai.Client(api_key=AI_API_KEY)



def build_job_prompt(profile_id: str, job_text: str) -> str:
    profile_prompt = build_profile_prompt(profile_id)
    return f"""
Analyze this job against the selected user profile.

User profile:
{profile_prompt}

Job description:
{job_text}

Return JSON only.

Score:
0 = no fit
1 = weak fit
2 = partial fit
3 = decent fit
4 = strong fit
5 = excellent fit

Consider:
- job title relevance
- internship/junior seniority fit
- location and work mode
- skill match
- salary if available
- avoid keywords from the profile
- target professional areas from the profile

***EXTREMELY IMPORTANTE: If the job description contains any of the avoid keywords from the profile, the score should be 0, regardless of any other factor.
ALSO: If the job doesn't fit the target professional areas from the profile, the score should be 0.***

Also extract short fields for a Telegram announcement.
Do not write the full announcement. Fill only the JSON fields.
"""


def format_job_text(job: dict) -> str:
    return (
        f"Title: {job.get('title', 'N/A')}\n"
        f"Company: {job.get('company', 'N/A')}\n"
        f"Salary: {job.get('salary', 'N/A')}\n"
        f"Published: {job.get('published', 'N/A')}\n"
        f"Location / mode: {job.get('location', 'N/A')}\n"
        f"Description: {job.get('description', 'N/A')}\n"
        f"URL: {job.get('url', 'N/A')}\n"
    )


def score_job(profile_id: str, input_text: str, client, model: str = "gemini-3.1-flash-lite") -> JobScore:
    prompt = build_job_prompt(profile_id, input_text)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": JobScore.model_json_schema(),
        },
    )
    
    return JobScore.model_validate_json(response.text)


def score_silver_job(profile_id: str, job: dict, client, model: str = "gemini-3.1-flash-lite") -> dict:
    input_text = format_job_text(job)
    score = score_job(profile_id, input_text, client, model)
    scored_job = {
        **job,
        "profile_id": profile_id,
        "score": score.score,
        "opportunity_type": score.opportunity_type,
        "area": score.area,
        "focus": score.focus,
        "tools": score.tools,
    }
    upsert_gold_job(scored_job)
    return scored_job


def score_silver_jobs_from_db(profile_id: str, client, limit: int = 10, model: str = "gemini-3.1-flash-lite") -> list[dict]:
    jobs = get_silver_jobs(limit)
    scored_jobs = []
    for job in jobs:
        scored_jobs.append(score_silver_job(profile_id, job, client, model))
    return scored_jobs
