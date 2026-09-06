from ai.prompts import CAREER_CHAT_SYSTEM_PROMPT


def _build_transcript(history: list) -> str:
    """
    Turns [{"role": "user"/"assistant", "content": "..."}] into a plain-text
    transcript. Kept simple on purpose — works with any provider's single
    prompt + system_prompt interface without needing per-provider chat APIs.
    """
    lines = []
    for turn in history:
        speaker = "User" if turn.get("role") == "user" else "CareerPilot AI"
        lines.append(f"{speaker}: {turn.get('content', '')}")
    return "\n".join(lines)


def chat_with_assistant(
    manager,
    history: list,
    user_message: str,
    user_context: dict = None,
) -> str:
    """
    history: list of {"role": "user"|"assistant", "content": str} — prior turns.
    user_message: the new message from the user.
    user_context: optional dict (target_role, skills, experience_level, etc.)
                  that the user has explicitly provided/confirmed, used to
                  personalize the reply — never invented by the AI.
    Returns the assistant's reply text. Caller is responsible for appending
    both the user_message and the returned reply to `history` afterward.
    """
    transcript = _build_transcript(history)

    context_block = ""
    if user_context:
        context_lines = [f"- {k}: {v}" for k, v in user_context.items() if v]
        if context_lines:
            context_block = (
                "\nKnown facts about this user (only use what's listed, "
                "don't assume more):\n" + "\n".join(context_lines) + "\n"
            )

    prompt = (
        f"{context_block}\n"
        f"Conversation so far:\n{transcript}\n\n"
        f"User: {user_message}\n"
        f"CareerPilot AI:"
    ).strip()

    return manager.generate(
        prompt,
        system_prompt=CAREER_CHAT_SYSTEM_PROMPT,
        max_tokens=800,
    ).strip()
