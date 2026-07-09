from apps.jobs.exceptions import (
    InvalidJobProviderException,
)

from apps.jobs.providers.remoteok_provider import (
    RemoteOKProvider,
)

# from apps.jobs.providers.adzuna_provider import (
#     AdzunaProvider,
# )

# from apps.jobs.providers.jooble_provider import (
#     JoobleProvider,
# )


class JobProviderFactory:

    PROVIDERS = {

        "remoteok": RemoteOKProvider,

        # "adzuna": AdzunaProvider,

        # "jooble": JoobleProvider,

    }

    @classmethod
    def get_provider(
        cls,
        provider_name: str,
    ):

        provider = cls.PROVIDERS.get(
            provider_name.lower()
        )

        if provider is None:

            raise InvalidJobProviderException(
                f"{provider_name} is not supported."
            )

        return provider()