import logging
from abc import ABC, abstractmethod

import requests

from apps.jobs.exceptions import JobProviderException


logger = logging.getLogger(__name__)


class BaseJobProvider(ABC):
    """
    Base class for all job providers.
    """

    DEFAULT_TIMEOUT = 15

    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "User-Agent": "AI-Resume-Analyzer/1.0",
    }

    def get(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> dict | list:

        request_headers = self.DEFAULT_HEADERS.copy()

        if headers:
            request_headers.update(headers)

        try:

            response = requests.get(
                url=url,
                params=params,
                headers=request_headers,
                timeout=self.DEFAULT_TIMEOUT,
            )

            response.raise_for_status()

            return response.json()

        except requests.Timeout as exc:

            logger.exception("Job provider timeout.")

            raise JobProviderException(
                "Job provider request timed out."
            ) from exc

        except requests.HTTPError as exc:

            logger.exception("HTTP error.")

            raise JobProviderException(
                f"HTTP Error: {exc}"
            ) from exc

        except requests.RequestException as exc:

            logger.exception("Network error.")

            raise JobProviderException(
                "Unable to connect to job provider."
            ) from exc

    @abstractmethod
    def search_jobs(
        self,
        *,
        role: str,
        location: str,
        skills: list[str],
    ):

        raise NotImplementedError