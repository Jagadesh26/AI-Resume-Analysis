import logging
import os

from openai import OpenAI

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class OpenRouterProvider(BaseAIProvider):
    """
    OpenRouter Provider
    """

    def __init__(self):

        api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not api_key:
            raise AIProviderException(
                "OpenRouter API key is not configured."
            )

        self.client = OpenAI(

            api_key=api_key,

            base_url="https://openrouter.ai/api/v1",

        )

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "deepseek/deepseek-chat",
        )

    @staticmethod
    def _format_error_message(exc: Exception) -> str:

        message = str(exc).strip()

        if not message:
            return "OpenRouter request failed."

        if "401" in message:
            return "Invalid OpenRouter API key."

        if "429" in message:
            return "OpenRouter rate limit exceeded."

        return f"OpenRouter request failed: {message}"

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
                    "OpenRouter returned an empty response."
                )

            raw_text = content.strip() if isinstance(content, str) else str(content)

            return AIProviderResponse(
                provider="openrouter",
                model=self.model,
                raw_text=raw_text,
                usage=None,
            )

        except Exception as exc:

            logger.exception(
                "OpenRouter provider request failed."
            )

            raise AIProviderException(
                self._format_error_message(exc)
            ) from exc