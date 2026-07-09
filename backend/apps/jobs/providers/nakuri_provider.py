from __future__ import annotations

import logging

import requests

from apps.jobs.providers.base_provider import BaseJobProvider
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.normalization_service import (
    NormalizationService,
)

logger = logging.getLogger(__name__)


class NaukriProvider(BaseJobProvider):
    """
    Naukri Job Provider
    """

    source_name = "Naukri"

    base_url = "https://www.naukri.com"

    API_URL = "https://www.naukri.com/jobapi/v3/search"

    PAGE_SIZE = 20

    MAX_PAGES = 5

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

        "Referer": "https://www.naukri.com/",

    }

    def search_jobs(
        self,
        *,
        role: str,
        location: str = "",
        skills: list[str] | None = None,
    ) -> list[JobSchema]:

        jobs: list[JobSchema] = []

        seo_key = (
            role.lower()
            .replace(" ", "-")
        )

        for page in range(
            1,
            self.MAX_PAGES + 1,
        ):

            params = {

                "noOfResults": self.PAGE_SIZE,

                "urlType": "search_by_keyword",

                "searchType": "adv",

                "keyword": role,

                "location": location,

                "pageNo": page,

                "k": role,

                "l": location,

                "seoKey": seo_key,

                "src": "jobsearchDesk",

                "latLong": "",

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
                    "Naukri API request failed. "
                    "Role=%s Page=%s",
                    role,
                    page,
                )

                continue

            raw_jobs = payload.get(
                "jobDetails",
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
                        "Failed to normalize "
                        "Naukri job."
                    )

        return jobs

    def normalize(
        self,
        raw_job: dict,
    ) -> JobSchema:

        return (
            NormalizationService
            .normalize_naukri(
                raw_job
            )
        )