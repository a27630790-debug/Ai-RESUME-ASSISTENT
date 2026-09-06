import json
import re


def extract_json(text: str) -> dict:
    """
    Safely extract a JSON object from AI text output, even when the model
    wraps it in markdown code fences or adds extra commentary around it.
    Raises ValueError with the raw text included, so callers can log/debug
    instead of crashing with a confusing JSONDecodeError.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"AI did not return valid JSON.\nError: {e}\nRaw output:\n{text}"
        ) from e
