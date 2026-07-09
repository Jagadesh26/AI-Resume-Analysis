import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.jobs.providers.provider_factory import JobProviderFactory
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.ranking_service import RankingService
from apps.jobs.services.deduplication_service import (
    DeduplicationService,
)


logger = logging.getLogger(__name__)


class JobSearchService:
    """
    Searches jobs from multiple providers,
    removes duplicates,
    ranks them,
    and returns the best matches.
    """

    DEFAULT_PROVIDERS = (
        "remoteok",
        # "adzuna",
        # "jooble",
    )

    @classmethod
    def search_jobs(
        cls,
        *,
        roles: list[str],
        preferred_location: str,
        skills: list[str],
        experience_level: str,
        work_modes: list[str],
        limit: int = 20,
    ) -> list[JobSchema]:

        jobs: list[JobSchema] = []

        with ThreadPoolExecutor(
            max_workers=len(cls.DEFAULT_PROVIDERS),
        ) as executor:

            futures = []

            for provider_name in cls.DEFAULT_PROVIDERS:

                provider = JobProviderFactory.get_provider(
                    provider_name,
                )

                for role in roles:

                    futures.append(

                        executor.submit(

                            provider.search_jobs,

                            role=role,

                            location=preferred_location,

                            skills=skills,

                        )

                    )

            for future in as_completed(futures):

                try:

                    provider_jobs = future.result()

                    jobs.extend(provider_jobs)

                except Exception:

                    logger.exception(
                        "Job provider failed."
                    )

        jobs = DeduplicationService.remove_duplicates(
            jobs
        )

        jobs = RankingService.rank_jobs(

            jobs=jobs,

            roles=roles,

            location=preferred_location,

            skills=skills,

            experience=experience_level,

            work_modes=work_modes,

        )

        return jobs[:limit]