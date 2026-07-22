from apps.ai.providers.base_openrouter_provider import (
    BaseOpenRouterProvider,
)


class QwenProvider(
    BaseOpenRouterProvider
):
    """
    Qwen Provider
    Powered by OpenRouter.
    """

    provider_name = "qwen"

    MODEL_NAME = "qwen/qwen3-235b-a22b:free"

    model = MODEL_NAME