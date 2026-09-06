from ai.base_provider import BaseAIProvider
from config.settings import get_secret, GEMINI_API_KEY_NAME, GEMINI_MODEL


class GeminiProvider(BaseAIProvider):
    name = "gemini"

    def __init__(self):
        # ============================================================
        # 🔑 API KEY LOADED HERE — actual value comes from Colab Secrets
        # (left sidebar -> key icon -> add secret "GEMINI_API_KEY")
        # ============================================================
        self.api_key = get_secret(GEMINI_API_KEY_NAME)
        self._client_ready = False
        self._genai = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._genai = genai
                self._client_ready = True
            except Exception:
                self._client_ready = False

    def is_configured(self) -> bool:
        return self._client_ready

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 1024) -> str:
        if not self._client_ready:
            raise RuntimeError("Gemini not configured (missing/invalid API key)")

        model = self._genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=system_prompt or None,
        )
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_tokens},
        )
        if not getattr(response, "text", None):
            raise RuntimeError("Gemini returned an empty response")
        return response.text
