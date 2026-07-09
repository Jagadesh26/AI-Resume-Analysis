import os
import logging

from google import genai

from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.exceptions import AIProviderException
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise AIProviderException(
                "AI provider is not configured."
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

    def analyze(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if not response.text:
                raise AIProviderException(
                    "Gemini returned an empty response."
                )

            return AIProviderResponse(
                provider="gemini",
                model=self.model,
                raw_text=response.text.strip(),
                usage=None,
            )

        except Exception as exc:
            logger.exception("Gemini provider request failed.")

            raise AIProviderException(
                "Gemini request failed."
            ) from exc
