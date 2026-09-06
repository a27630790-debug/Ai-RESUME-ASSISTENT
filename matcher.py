from ai.prompts import JOB_MATCH_JSON_PROMPT
from utils.ai_json import generate_structured_json

SYSTEM_PROMPT = (
    "You are CareerPilot AI's resume-to-job matching engine. You NEVER credit "
    "the candidate with skills or experience that are not present in their "
    "resume text — only compare what is actually there."
)


def match_resume_to_job(manager, resume_text: str, jd_text: str) -> dict:
    """
    Returns a dict with keys: match_percentage, matching_skills,
    missing_skills, matching_keywords, missing_keywords, experience_gap,
    education_match, strengths, weaknesses, recommendations.
    """
    prompt = JOB_MATCH_JSON_PROMPT.format(resume_text=resume_text, jd_text=jd_text)
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1500)
