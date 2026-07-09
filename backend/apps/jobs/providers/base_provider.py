from __future__ import annotations

from abc import ABC, abstractmethod

from apps.jobs.schemas.job_schema import JobSchema


class BaseJobProvider(ABC):
    """
    Base class for every job provider.

    Every provider (Naukri, Foundit, RemoteOK, LinkedIn, etc.)
    must implement these methods.

    The contract is simple:

    search_jobs()
            ↓
    fetch provider API
            ↓
    normalize raw jobs
            ↓
    return List[JobSchema]
    """

    source_name: str = ""

    base_url: str = ""

    @abstractmethod
    def search_jobs(
        self,
        *,
        role: str,
        location: str = "",
        skills: list[str] | None = None,
    ) -> list[JobSchema]:
        """
        Search jobs from the provider.

        Must always return normalized JobSchema objects.
        """
        raise NotImplementedError

    @abstractmethod
    def normalize(
        self,
        raw_job: dict,
    ) -> JobSchema:
        """
        Convert provider response into JobSchema.
        """
        raise NotImplementedError