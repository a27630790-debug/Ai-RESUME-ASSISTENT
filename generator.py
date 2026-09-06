from ai.prompts import COVER_LETTER_PROMPT

SYSTEM_PROMPT = (
    "You are CareerPilot AI's cover letter writer. You ONLY use real "
    "information found in the candidate's resume. You NEVER invent "
    "experience, skills, or achievements."
)


def generate_cover_letter(
    manager,
    resume_text: str,
    jd_text: str,
    company: str = "",
    role: str = "",
    tone: str = "professional",
    length: str = "medium (3-4 paragraphs)",
) -> str:
    """Returns the cover letter as plain text, ready to send."""
    prompt = COVER_LETTER_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text,
        company=company or "the company",
        role=role or "the role",
        tone=tone,
        length=length,
    )
    return manager.generate(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=900).strip()
