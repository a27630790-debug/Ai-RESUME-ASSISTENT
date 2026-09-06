from ai.prompts import RESUME_TAILORING_JSON_PROMPT
from utils.ai_json import generate_structured_json

SYSTEM_PROMPT = (
    "You are CareerPilot AI's resume tailoring engine. You ONLY reorganize and "
    "rephrase information that already exists in the candidate's resume. You "
    "NEVER invent skills, employers, projects, numbers, or achievements."
)


def tailor_resume_to_job(manager, resume_text: str, jd_text: str) -> dict:
    """
    Returns a dict with keys: tailored_summary, prioritized_skills,
    rewritten_bullets (list of {original, tailored}), keywords_to_naturally_add,
    sections_to_deprioritize.
    """
    prompt = RESUME_TAILORING_JSON_PROMPT.format(resume_text=resume_text, jd_text=jd_text)
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1800)
