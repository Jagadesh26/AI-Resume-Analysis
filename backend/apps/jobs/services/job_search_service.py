from __future__ import annotations

import logging
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from apps.jobs.providers.provider_factory import (
    JobProviderFactory,
)
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.deduplication_service import (
    DeduplicationService,
)
from apps.jobs.services.ranking_service import (
    RankingService,
)

logger = logging.getLogger(__name__)


class JobSearchService:
    """
    Aggregates jobs from all providers,
    removes duplicates,
    ranks them,
    and returns the best matches.
    """

    @classmethod
    def search_jobs(
        cls,
        *,
        roles: list[str],
        preferred_location: str = "",
        skills: list[str] | None = None,
        experience_level: str = "",
        work_modes: list[str] | None = None,
        limit: int = 20,
    ) -> list[JobSchema]:

        skills = skills or []

        work_modes = work_modes or []

        providers = JobProviderFactory.get_all_providers()

        jobs: list[JobSchema] = []

        futures = []

        with ThreadPoolExecutor(
            max_workers=len(providers),
        ) as executor:

            for provider in providers:

                for role in roles:

                    futures.append(

                        executor.submit(

                            provider.search_jobs,

                            role=role,

                            location=preferred_location,

                            skills=skills,

                        )

                    )

            for future in as_completed(
                futures
            ):

                try:

                    jobs.extend(
                        future.result()
                    )

                except Exception:

                    logger.exception(
                        "Provider search failed."
                    )

        jobs = (
            DeduplicationService
            .remove_duplicates(
                jobs
            )
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