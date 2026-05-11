from pydantic import BaseModel, Field

prompt = """
Analyze this job against the selected user profile.

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

Also extract short fields for a Telegram announcement.
Do not write the full announcement. Fill only the JSON fields.
"""


class JobScore(BaseModel):
    score: int = Field(description="0 to 5 match score")
    opportunity_type: str = Field(description="Example: estágio, vaga júnior, trainee")
    area: str = Field(description="Main professional area")
    focus: str = Field(description="Main work focus")
    tools: list[str] = Field(description="Main technologies, tools, or skills")

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[prompt, input_text],
    config={
        "response_mime_type": "application/json",
        "response_json_schema": JobScore.model_json_schema(),
    },
)

print(response.text)
