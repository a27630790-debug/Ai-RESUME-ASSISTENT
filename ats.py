from ai.prompts import ATS_ANALYSIS_JSON_PROMPT
from utils.ai_json import generate_structured_json

SYSTEM_PROMPT = (
    "You are CareerPilot AI's ATS analysis engine. Scores are ESTIMATES only, "
    "never a real company's actual ATS score. You NEVER invent resume content — "
    "you only analyze what is present in the text given to you."
)


def analyze_ats_score(manager, resume_text: str) -> dict:
    """
    Returns a dict with keys: ats_score, score_label, keyword_optimization,
    formatting_issues, missing_sections, recommendations.
    """
    prompt = ATS_ANALYSIS_JSON_PROMPT.format(resume_text=resume_text)
    return generate_structured_json(manager, prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1200)
