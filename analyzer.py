from ai.prompts import (
    RESUME_ANALYSIS_PROMPT, ATS_ANALYSIS_PROMPT,
    JOB_MATCH_PROMPT, RESUME_REWRITE_BULLET_PROMPT,
)

SYSTEM_PROMPT = (
    "You are CareerPilot AI, a professional and honest resume/career assistant. "
    "You NEVER invent facts, experience, skills, employers, or achievements not "
    "present in the user's own text."
)


def analyze_resume(manager, resume_text: str) -> str:
    prompt = RESUME_ANALYSIS_PROMPT.format(resume_text=resume_text)
    return manager.generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1500)


def analyze_ats(manager, resume_text: str) -> str:
    prompt = ATS_ANALYSIS_PROMPT.format(resume_text=resume_text)
    return manager.generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1000)


def match_job(manager, resume_text: str, job_description: str) -> str:
    prompt = JOB_MATCH_PROMPT.format(resume_text=resume_text, job_description=job_description)
    return manager.generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1500)


def rewrite_bullet(manager, bullet_text: str) -> str:
    prompt = RESUME_REWRITE_BULLET_PROMPT.format(bullet_text=bullet_text)
    return manager.generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=200).strip()
