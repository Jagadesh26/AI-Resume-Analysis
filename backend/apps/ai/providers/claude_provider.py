import os
import logging

import anthropic

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.base_provider import BaseAIProvider
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class ClaudeProvider(BaseAIProvider):
    """
    Claude Provider
    """

    def __init__(self):

        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise AIProviderException(
                "AI provider is not configured."
            )

        self.client = anthropic.Anthropic(
            api_key=api_key
        )

        self.model = os.getenv(
            "CLAUDE_MODEL",
            "claude-sonnet-4-6",
        )

    def analyze(self, prompt: str) -> str:

        try:

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            if not response.content:
                raise AIProviderException(
                    "Claude returned an empty response."
                )

            return AIProviderResponse(
                provider="claude",
                model=self.model,
                raw_text=response.content[0].text.strip(),
                usage=None,
            )

        except Exception as exc:
            logger.exception("Claude provider request failed.")

            raise AIProviderException(
                "Claude request failed."
            ) from exc
