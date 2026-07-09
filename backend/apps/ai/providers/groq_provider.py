import logging
import os

from groq import Groq

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class GroqProvider(BaseAIProvider):
    """
    Groq AI Provider
    """

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise AIProviderException(
                "Groq API key is not configured."
            )

        self.client = Groq(
            api_key=api_key,
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    @staticmethod
    def _format_error_message(exc: Exception) -> str:

        message = str(exc).strip()

        if not message:
            return "Groq request failed."

        if "rate limit" in message.lower():
            return "Groq rate limit exceeded."

        if "authentication" in message.lower():
            return "Invalid Groq API key."

        return f"Groq request failed: {message}"

    def analyze(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                temperature=0.2,

                max_tokens=4096,

            )

            content = response.choices[0].message.content

            if not content:
                raise AIProviderException(
                    "Groq returned an empty response."
                )

            raw_text = content.strip() if isinstance(content, str) else str(content)

            return AIProviderResponse(
                provider="groq",
                model=self.model,
                raw_text=raw_text,
                usage=None,
            )

        except Exception as exc:

            logger.exception(
                "Groq provider request failed."
            )

            raise AIProviderException(
                self._format_error_message(exc)
            ) from exc