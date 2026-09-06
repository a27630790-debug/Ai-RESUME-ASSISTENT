from ai.prompts import CAREER_ROADMAP_JSON_PROMPT
from utils.ai_json import generate_structured_json

SYSTEM_PROMPT = (
    "You are CareerPilot AI's roadmap planning engine. You ONLY use the "
    "profile information given to you — never invent the user's skills, "
    "education, or experience."
)


def generate_roadmap(manager, profile: dict, duration_days: int = 90) -> dict:
    """
    profile keys (all optional, pass what the user has actually given):
      education, skills, experience, interests, target_role
    duration_days: typically 30, 60, or 90

    Returns a dict: {duration_days, target_role, phases: [...]}
    """
    prompt = CAREER_ROADMAP_JSON_PROMPT.format(
        education=profile.get("education", "Not specified"),
        skills=profile.get("skills", "Not specified"),
        experience=profile.get("experience", "Not specified"),
        interests=profile.get("interests", "Not specified"),
        target_role=profile.get("target_role", "Not specified"),
        duration_days=duration_days,
    )
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=2000)
