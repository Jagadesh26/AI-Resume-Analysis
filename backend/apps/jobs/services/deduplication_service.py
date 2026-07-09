from __future__ import annotations

from apps.jobs.schemas.job_schema import JobSchema


class DeduplicationService:
    """
    Removes duplicate jobs collected from multiple providers.
    """

    @classmethod
    def remove_duplicates(
        cls,
        jobs: list[JobSchema],
    ) -> list[JobSchema]:

        unique_jobs: dict[
            tuple[str, str, str],
            JobSchema,
        ] = {}

        for job in jobs:

            key = cls._build_key(job)

            existing = unique_jobs.get(key)

            if existing is None:

                unique_jobs[key] = job

                continue

            if cls._is_better(job, existing):

                unique_jobs[key] = job

        return list(unique_jobs.values())

    @staticmethod
    def _build_key(
        job: JobSchema,
    ) -> tuple[str, str, str]:

        title = (
            job.job_title
            .strip()
            .lower()
        )

        company = (
            job.company
            .strip()
            .lower()
        )

        location = (
            job.location
            .strip()
            .lower()
        )

        return (
            title,
            company,
            location,
        )

    @staticmethod
    def _is_better(
        new_job: JobSchema,
        existing_job: JobSchema,
    ) -> bool:
        """
        Prefer the richer job record.
        """

        new_score = 0
        old_score = 0

        fields = [

            "description",

            "salary",

            "experience",

            "skills",

            "apply_url",

        ]

        for field in fields:

            if getattr(new_job, field):

                new_score += 1

            if getattr(existing_job, field):

                old_score += 1

        return new_score > old_score