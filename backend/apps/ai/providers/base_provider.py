from abc import ABC, abstractmethod

from apps.ai.providers.provider_response import AIProviderResponse



class BaseAIProvider(ABC):
    """
    Base class for all AI providers.
    """

    @abstractmethod
    def analyze(
        self,
        prompt: str,
    ) -> AIProviderResponse:
        """
        Send prompt to AI provider
        and return the raw text response.
        """
        raise NotImplementedError


BaseProvider = BaseAIProvider
