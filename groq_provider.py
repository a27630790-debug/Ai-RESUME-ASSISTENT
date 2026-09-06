from ai.base_provider import BaseAIProvider
from config.settings import get_secret, GROQ_API_KEY_NAME, GROQ_MODEL


class GroqProvider(BaseAIProvider):
    name = "groq"

    def __init__(self):
        # ============================================================
        # 🔑 API KEY LOADED HERE — actual value comes from Colab Secrets
        # (left sidebar -> key icon -> add secret "GROQ_API_KEY")
        # ============================================================
        self.api_key = get_secret(GROQ_API_KEY_NAME)
        self._client = None
        self._client_ready = False

        if self.api_key:
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
                self._client_ready = True
            except Exception:
                self._client_ready = False

    def is_configured(self) -> bool:
        return self._client_ready

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 1024) -> str:
        if not self._client_ready:
            raise RuntimeError("Groq not configured (missing/invalid API key)")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = self._client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=max_tokens,
        )
        content = completion.choices[0].message.content
        if not content:
            raise RuntimeError("Groq returned an empty response")
        return content
