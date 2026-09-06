from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """
    Every AI provider (Gemini, Groq, and any future provider) must implement
    this interface. This is what makes the fallback system provider-agnostic —
    adding a new provider later never requires rewriting the app.
    """

    name = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if this provider has a valid API key and is ready to use."""
        ...

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 1024) -> str:
        """Return generated text. Raise an exception on any failure (quota, network, etc.)."""
        ...
