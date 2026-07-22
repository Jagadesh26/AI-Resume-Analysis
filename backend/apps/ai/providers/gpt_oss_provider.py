from apps.ai.providers.base_openrouter_provider import (
    BaseOpenRouterProvider,
)


class GPTOSSProvider(
    BaseOpenRouterProvider
):
    """
    GPT-OSS Provider
    Powered by OpenRouter.
    """

    provider_name = "gpt-oss"

    model = "openai/gpt-oss-120b"