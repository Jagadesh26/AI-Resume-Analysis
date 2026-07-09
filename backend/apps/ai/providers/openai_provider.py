import os
import logging

from openai import OpenAI

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI Provider
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise AIProviderException(
                "AI provider is not configured."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.4-mini",
        )

    @staticmethod
    def _format_error_message(exc: Exception) -> str:
        message = str(exc).strip()

        if not message:
            return "OpenAI request failed."

        if "quota" in message.lower() or "insufficient_quota" in message.lower():
            return (
                "OpenAI request failed because your account quota is exhausted or billing is not configured. "
                f"Details: {message}"
            )

        return f"OpenAI request failed: {message}"

    def analyze(self, prompt: str) -> str:

        try:

            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )

            if not response.output_text:
                raise AIProviderException(
                    "OpenAI returned an empty response."
                )

            return AIProviderResponse(
                provider="openai",
                model=self.model,
                raw_text=response.output_text.strip(),
                usage=response.usage.model_dump()
                if getattr(response, "usage", None)
                else None,
            )

        except Exception as exc:
            logger.exception("OpenAI provider request failed.")

            raise AIProviderException(
                self._format_error_message(exc)
            ) from exc
