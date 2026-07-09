from apps.jobs.schemas.job_schema import JobSchema


class DeduplicationService:
    """
    Removes duplicate jobs.
    """

    @staticmethod
    def remove_duplicates(
        jobs: list[JobSchema],
    ) -> list[JobSchema]:

        unique = {}

        for job in jobs:

            key = (

                job.job_title.lower(),

                job.company.lower(),

                job.location.lower(),

            )

            unique[key] = job

        return list(unique.values())