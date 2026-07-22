from apps.ai.providers.gemini_provider import GeminiProvider
from apps.ai.providers.groq_provider import GroqProvider
from apps.ai.providers.openai_provider import OpenAIProvider
from apps.ai.providers.claude_provider import ClaudeProvider

from apps.ai.providers.gpt_oss_provider import (
    GPTOSSProvider,
)

from apps.ai.providers.qwen_provider import (
    QwenProvider,
)

from apps.ai.exceptions import InvalidProviderException
from apps.ai.providers.openrouter_provider import OpenRouterProvider


class ProviderFactory:

    PROVIDERS = {

        "gemini": GeminiProvider,

        "groq": GroqProvider,

        "openrouter": OpenRouterProvider,

        "openai": OpenAIProvider,

        "claude": ClaudeProvider,

        "gpt-oss": GPTOSSProvider,

        "qwen": QwenProvider,

    }

    @classmethod
    def get_provider(cls, provider_name: str):

        provider = cls.PROVIDERS.get(
            provider_name.lower()
        )

        if provider is None:

            raise InvalidProviderException(
                f"{provider_name} is not supported."
            )

        return provider()