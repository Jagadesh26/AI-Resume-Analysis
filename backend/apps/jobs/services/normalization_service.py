from __future__ import annotations

import re

from apps.jobs.schemas.job_schema import JobSchema
from datetime import datetime


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

        location = ""

        if job.get("locations"):

            location = ", ".join(

                loc.get("city", "")

                for loc in job["locations"]

                if loc.get("city")

            )

        experience = ""

        minimum = (
            job.get("minimumExperience", {})
            .get("years")
        )

        maximum = (
            job.get("maximumExperience", {})
            .get("years")
        )

        if minimum is not None and maximum is not None:

            experience = f"{minimum}-{maximum} Years"

        elif minimum is not None:

            experience = f"{minimum}+ Years"

        salary = ""

        minimum_salary = (
            job.get("minimumSalary", {})
            .get("absoluteValue")
        )

        maximum_salary = (
            job.get("maximumSalary", {})
            .get("absoluteValue")
        )

        if minimum_salary and maximum_salary:

            salary = (
                f"{minimum_salary:,}"
                f" - "
                f"{maximum_salary:,} INR"
            )

        return JobSchema(

            job_title=job.get(
                "title",
                "",
            ),

            company=(
                job.get("company", {})
                .get("name", "")
            ),

            location=location,

            experience=experience,

            employment_type=(
                job.get(
                    "employmentTypes",
                    ["Full Time"],
                )[0]
                if job.get("employmentTypes")
                else ""
            ),

            work_mode=cls.detect_work_mode(
                job.get(
                    "description",
                    "",
                )
            ),

            salary=salary,

            description=job.get(
                "description",
                "",
            ),

            skills=cls.extract_foundit_skills(
                job
            ),

            posted_date=cls.format_timestamp(
                job.get(
                    "postedAt",
                )
            ),

            apply_url=(
                f"https://www.foundit.in"
                f"{job.get('jdUrl','')}"
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
    


    @staticmethod
    def extract_foundit_skills(
        job: dict,
    ) -> list[str]:

        skills = []

        for skill in job.get(
            "skills",
            [],
        ):

            if isinstance(
                skill,
                dict,
            ):

                if skill.get("text"):

                    skills.append(
                        skill["text"]
                    )

        for skill in job.get(
            "itSkills",
            [],
        ):

            if isinstance(
                skill,
                dict,
            ):

                if skill.get("text"):

                    skills.append(
                        skill["text"]
                    )

        return list(
            dict.fromkeys(
                skills
            )
        )



    @staticmethod
    def format_timestamp(
        timestamp,
    ) -> str:

        if not timestamp:

            return ""

        return datetime.fromtimestamp(
            timestamp / 1000
        ).strftime("%Y-%m-%d")
    


    @staticmethod
    def detect_work_mode(
        description: str,
    ) -> str:

        text = description.lower()

        if "remote" in text:

            return "Remote"

        if "hybrid" in text:

            return "Hybrid"

        return "Onsite"