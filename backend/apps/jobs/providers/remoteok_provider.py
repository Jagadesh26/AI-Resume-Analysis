from __future__ import annotations

import logging
import requests

from apps.jobs.providers.base_provider import BaseJobProvider
from apps.jobs.schemas.job_schema import JobSchema
from apps.jobs.services.normalization_service import (
    NormalizationService,
)

logger = logging.getLogger(__name__)


class RemoteOKProvider(BaseJobProvider):
    """
    RemoteOK Job Provider.
    """

    source_name = "RemoteOK"

    base_url = "https://remoteok.com"

    API_URL = "https://remoteok.com/api"

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

    }

    TIMEOUT = 30

    def search_jobs(
        self,
        *,
        role: str,
        location: str = "",
        skills: list[str] | None = None,
    ) -> list[JobSchema]:

        jobs: list[JobSchema] = []

        try:

            response = requests.get(

                self.API_URL,

                headers=self.HEADERS,

                timeout=self.TIMEOUT,

            )

            response.raise_for_status()

            payload = response.json()

        except Exception:

            logger.exception(
                "Failed to fetch RemoteOK jobs."
            )

            return jobs

        if not isinstance(payload, list):

            return jobs

        # First element contains metadata.
        payload = payload[1:]

        role = role.lower()

        for raw_job in payload:

            title = raw_job.get(
                "position",
                "",
            ).lower()

            if role not in title:
                continue

            try:

                jobs.append(
                    self.normalize(raw_job)
                )

            except Exception:

                logger.exception(
                    "Failed to normalize RemoteOK job."
                )

        return jobs

    def normalize(
        self,
        raw_job: dict,
    ) -> JobSchema:

        return (
            NormalizationService
            .normalize_remoteok(
                raw_job
            )
        )