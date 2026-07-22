import logging
import os

from openai import OpenAI

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class BaseOpenRouterProvider(BaseAIProvider):
    """
    Base class for all OpenRouter models.
    """

    model = None

    def __init__(self):

        api_key = os.getenv(
            "OPENROUTER_API_KEY",
        )

        if not api_key:

            raise AIProviderException(
                "OpenRouter API key is not configured."
            )

        self.client = OpenAI(

            api_key=api_key,

            base_url="https://openrouter.ai/api/v1",

        )

        if not self.model:

            raise AIProviderException(
                "Model is not configured."
            )

    @staticmethod
    def _format_error_message(
        exc: Exception,
    ) -> str:

        message = str(exc).strip()

        if not message:

            return "OpenRouter request failed."

        return (
            f"OpenRouter request failed: "
            f"{message}"
        )

    def analyze(
        self,
        prompt: str,
    ) -> AIProviderResponse:

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

            )

            text = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            usage = None

            if getattr(response, "usage", None):

                usage = {

                    "prompt_tokens":
                        response.usage.prompt_tokens,

                    "completion_tokens":
                        response.usage.completion_tokens,

                    "total_tokens":
                        response.usage.total_tokens,

                }

            return AIProviderResponse(

                provider=self.provider_name,

                model=self.model,

                raw_text=text,

                usage=usage,

            )

        except Exception as exc:

            logger.exception(
                "OpenRouter request failed."
            )

            raise AIProviderException(

                self._format_error_message(
                    exc
                )

            ) from exc