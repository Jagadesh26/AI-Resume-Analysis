from __future__ import annotations

import logging

import requests

from apps.jobs.providers.base_provider import BaseJobProvider
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.normalization_service import (
    NormalizationService,
)

logger = logging.getLogger(__name__)


class FounditProvider(BaseJobProvider):
    """
    Foundit Job Provider
    """

    source_name = "Foundit"

    base_url = "https://www.foundit.in"

    API_URL = (
        "https://www.foundit.in/home/api/searchResultsPage"
    )

    PAGE_SIZE = 20

    MAX_RESULTS = 100

    TIMEOUT = 30

    HEADERS = {

        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0.0.0 "
            "Safari/537.36"
        ),

        "Accept": "application/json",

        "Referer": "https://www.foundit.in/",

    }

    def search_jobs(
        self,
        *,
        role: str,
        location: str = "",
        skills: list[str] | None = None,
    ) -> list[JobSchema]:

        jobs: list[JobSchema] = []

        start = 0

        while start < self.MAX_RESULTS:

            params = {

                "query": role,

                "queryDerived": "true",

                "locations": location,

                "countries": "India",

                "variantName": "DEFAULT",

                "start": start,

                "limit": self.PAGE_SIZE,

            }

            try:

                response = requests.get(

                    self.API_URL,

                    params=params,

                    headers=self.HEADERS,

                    timeout=self.TIMEOUT,

                )

                response.raise_for_status()

                payload = response.json()

            except Exception:

                logger.exception(

                    "Foundit API request failed. "

                    "Role=%s Start=%s",

                    role,

                    start,

                )

                break

            raw_jobs = payload.get(

                "data",

                [],

            )

            if not raw_jobs:
                break

            for raw_job in raw_jobs:

                try:

                    jobs.append(

                        self.normalize(raw_job)

                    )

                except Exception:

                    logger.exception(

                        "Failed to normalize Foundit job."

                    )

            start += self.PAGE_SIZE

        return jobs

    def normalize(
        self,
        raw_job: dict,
    ) -> JobSchema:

        return (
            NormalizationService
            .normalize_foundit(
                raw_job
            )
        )