from __future__ import annotations

from apps.jobs.exceptions import InvalidJobProviderException

from apps.jobs.providers.base_provider import BaseJobProvider
from apps.jobs.providers.remoteok_provider import RemoteOKProvider

from apps.jobs.providers.foundit_provider import FounditProvider
from apps.jobs.providers.nakuri_provider import NaukriProvider


class JobProviderFactory:
    """
    Factory responsible for creating job provider instances.
    """

    PROVIDERS: dict[str, type[BaseJobProvider]] = {

        "remoteok": RemoteOKProvider,

        "naukri": NaukriProvider,

        "foundit": FounditProvider,

    }

    @classmethod
    def get_provider(
        cls,
        provider_name: str,
    ) -> BaseJobProvider:

        provider_class = cls.PROVIDERS.get(
            provider_name.lower()
        )

        if provider_class is None:

            supported = ", ".join(
                cls.PROVIDERS.keys()
            )

            raise InvalidJobProviderException(
                f"Unsupported provider '{provider_name}'. "
                f"Supported providers: {supported}"
            )

        return provider_class()

    @classmethod
    def get_all_providers(
        cls,
    ) -> list[BaseJobProvider]:

        return [

            provider()

            for provider in cls.PROVIDERS.values()

        ]