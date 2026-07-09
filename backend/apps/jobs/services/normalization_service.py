from apps.jobs.schemas.job_schema import JobSchema


class NormalizationService:

    @staticmethod
    def normalize_remoteok(
        job: dict,
    ) -> JobSchema:

        return JobSchema(

            job_title=job.get(
                "position",
                "",
            ),

            company=job.get(
                "company",
                "",
            ),

            location=job.get(
                "location",
                "Remote",
            ),

            experience="",

            employment_type="Full Time",

            work_mode="Remote",

            salary="",

            description=job.get(
                "description",
                "",
            ),

            skills=job.get(
                "tags",
                [],
            ),

            posted_date=job.get(
                "date",
                "",
            ),

            apply_url=(
                job.get("apply_url")
                or job.get("url")
                or ""
            ),

            source="RemoteOK",

            match_score=0,

            match_reason="",

        )
