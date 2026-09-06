from config.settings import PROVIDER_FALLBACK_ORDER
from ai.gemini_provider import GeminiProvider
from ai.groq_provider import GroqProvider


class AIProviderManager:
    """
    Central place the whole app talks to for any AI generation.
    Handles: automatic fallback, provider health, temporary disabling.
    Adding a future provider = write a new *_provider.py implementing
    BaseAIProvider, register it in self._providers, add its name to
    PROVIDER_FALLBACK_ORDER in config/settings.py. Nothing else changes.
    """

    def __init__(self):
        self._providers = {
            "gemini": GeminiProvider(),
            "groq": GroqProvider(),
        }
        self._disabled = set()          # temporarily disabled provider names
        self.last_used_provider = None
        self.last_error_log = []

    def _active_order(self):
        return [p for p in PROVIDER_FALLBACK_ORDER if p not in self._disabled]

    def disable_provider(self, name: str):
        self._disabled.add(name)

    def enable_provider(self, name: str):
        self._disabled.discard(name)

    def health_check(self) -> dict:
        """Returns which providers currently have a valid key configured."""
        return {name: p.is_configured() for name, p in self._providers.items()}

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 1024) -> str:
        errors = []
        for name in self._active_order():
            provider = self._providers.get(name)
            if not provider or not provider.is_configured():
                errors.append(f"{name}: not configured")
                continue
            try:
                result = provider.generate(prompt, system_prompt, max_tokens)
                self.last_used_provider = name
                return result
            except Exception as e:
                errors.append(f"{name}: {e}")
                continue  # try next provider in fallback order

        self.last_error_log = errors
        # This is the safe, user-facing message — raw errors are only in last_error_log
        raise RuntimeError(
            "AI service is temporarily busy. CareerPilot AI tried all available "
            "providers but none responded successfully."
        )
