from abc import ABC, abstractmethod

from google import genai

from app.core.config import settings


class BaseProvider(ABC):
    @abstractmethod
    def chat(self, message: str, system_prompt: str | None = None) -> str:
        pass


class GeminiProvider(BaseProvider):
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def chat(self, message: str, system_prompt: str | None = None) -> str:
        if system_prompt:
            message = f"{system_prompt}\n\nUser: {message}"

        res = self.client.models.generate_content(
            model=self.model,
            contents=message,
        )

        return res.text