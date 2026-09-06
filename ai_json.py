from utils.json_utils import extract_json


def generate_structured_json(
    manager,
    prompt: str,
    system_prompt: str = "",
    max_tokens: int = 1200,
    retries: int = 1,
) -> dict:
    """
    Calls manager.generate() and parses the result as JSON. If the AI
    returns invalid JSON (e.g. writes "thirty" instead of 30, or adds stray
    text), this automatically retries by telling the model exactly what was
    wrong and asking for a corrected version — instead of crashing the app.
    """
    last_error = None
    current_prompt = prompt

    for attempt in range(retries + 1):
        raw = manager.generate(current_prompt, system_prompt=system_prompt, max_tokens=max_tokens)
        try:
            return extract_json(raw)
        except ValueError as e:
            last_error = e
            if attempt < retries:
                current_prompt = (
                    f"{prompt}\n\n"
                    f"IMPORTANT: Your previous response was NOT valid JSON.\n"
                    f"Error: {e}\n"
                    f"Return ONLY corrected, valid JSON matching the exact "
                    f"schema above. All numeric fields must be real JSON "
                    f"numbers (e.g. 72), NEVER spelled-out words (e.g. never "
                    f"write 'seventy two' or 'thirty'). No markdown, no "
                    f"extra commentary — JSON only."
                )

    raise last_error
