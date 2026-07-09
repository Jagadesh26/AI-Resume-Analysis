from __future__ import annotations

import re

from apps.jobs.schemas.job_schema import JobSchema


class NormalizationService:
    """
    Converts provider-specific responses into JobSchema.

    Every provider should normalize its raw response here,
    so the rest of the application only works with JobSchema.
    """

    # ---------------------------------------------------------
    # Common Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _clean_string(value) -> str:

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _clean_html(text: str) -> str:

        if not text:
            return ""

        return re.sub(
            r"<[^>]+>",
            "",
            text,
        ).strip()

    @staticmethod
    def _to_list(value) -> list[str]:

        if not value:
            return []

        if isinstance(value, list):

            return [

                str(v).strip()

                for v in value

                if str(v).strip()

            ]

        if isinstance(value, str):

            return [

                skill.strip()

                for skill in value.split(",")

                if skill.strip()

            ]

        return []

    # =========================================================
    # RemoteOK
    # =========================================================

    @classmethod
    def normalize_remoteok(
        cls,
        job: dict,
    ) -> JobSchema:

        return JobSchema(

            job_title=cls._clean_string(
                job.get("position")
            ),

            company=cls._clean_string(
                job.get("company")
            ),

            location=cls._clean_string(
                job.get("location", "Remote")
            ),

            experience="",

            employment_type="Full Time",

            work_mode="Remote",

            salary=cls._clean_string(
                job.get("salary")
            ),

            description=cls._clean_html(
                job.get("description")
            ),

            skills=cls._to_list(
                job.get("tags")
            ),

            posted_date=cls._clean_string(
                job.get("date")
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

    # =========================================================
    # Naukri
    # =========================================================

    @classmethod
    def normalize_naukri(
        cls,
        job: dict,
    ) -> JobSchema:

        return JobSchema(

            job_title=cls._clean_string(
                job.get("title")
            ),

            company=cls._clean_string(
                job.get("companyName")
            ),

            location=cls._clean_string(
                job.get("placeholders", [{}])[0].get(
                    "label",
                    ""
                )
            ),

            experience=cls._clean_string(
                job.get("experienceText")
            ),

            employment_type="Full Time",

            work_mode=cls._detect_work_mode(
                job
            ),

            salary=cls._clean_string(
                job.get("salary")
            ),

            description=cls._clean_html(
                job.get("jobDescription")
            ),

            skills=cls._extract_naukri_skills(
                job
            ),

            posted_date=cls._clean_string(
                job.get("footerPlaceholderLabel")
            ),

            apply_url=cls._clean_string(
                job.get("jdURL")
            ),

            source="Naukri",

            match_score=0,

            match_reason="",

        )

    # =========================================================
    # Foundit
    # =========================================================

    @classmethod
    def normalize_foundit(
        cls,
        job: dict,
    ) -> JobSchema:

        return JobSchema(

            job_title=cls._clean_string(
                job.get("jobTitle")
            ),

            company=cls._clean_string(
                job.get("companyName")
            ),

            location=cls._clean_string(
                job.get("location")
            ),

            experience=cls._clean_string(
                job.get("experience")
            ),

            employment_type=cls._clean_string(
                job.get("employmentType")
            ),

            work_mode=cls._detect_foundit_work_mode(
                job
            ),

            salary=cls._clean_string(
                job.get("salary")
            ),

            description=cls._clean_html(
                job.get("jobDescription")
            ),

            skills=cls._to_list(
                job.get("skills")
            ),

            posted_date=cls._clean_string(
                job.get("postedDate")
            ),

            apply_url=cls._clean_string(
                job.get("jobDetailUrl")
            ),

            source="Foundit",

            match_score=0,

            match_reason="",

        )

    # =========================================================
    # Helper Methods
    # =========================================================

    @staticmethod
    def _extract_naukri_skills(
        job: dict,
    ) -> list[str]:

        skills = []

        for skill in job.get(
            "tagsAndSkills",
            [],
        ):

            if isinstance(skill, dict):

                value = skill.get("label")

                if value:
                    skills.append(value)

            elif isinstance(skill, str):

                skills.append(skill)

        return skills

    @staticmethod
    def _detect_work_mode(
        job: dict,
    ) -> str:

        text = str(job).lower()

        if "remote" in text:
            return "Remote"

        if "hybrid" in text:
            return "Hybrid"

        return "Onsite"

    @staticmethod
    def _detect_foundit_work_mode(
        job: dict,
    ) -> str:

        text = str(job).lower()

        if "remote" in text:
            return "Remote"

        if "hybrid" in text:
            return "Hybrid"

        return "Onsite"