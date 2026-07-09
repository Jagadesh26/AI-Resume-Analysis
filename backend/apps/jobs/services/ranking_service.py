from __future__ import annotations

import re

from apps.jobs.schemas.job_schema import JobSchema


class RankingService:
    """
    Scores jobs based on candidate preferences.
    """

    SKILL_WEIGHT = 50
    ROLE_WEIGHT = 25
    LOCATION_WEIGHT = 15
    EXPERIENCE_WEIGHT = 5
    WORKMODE_WEIGHT = 5

    @classmethod
    def rank_jobs(
        cls,
        *,
        jobs: list[JobSchema],
        roles: list[str],
        location: str,
        skills: list[str],
        experience: str,
        work_modes: list[str],
    ) -> list[JobSchema]:

        for job in jobs:

            skill_score = cls.skill_score(
                skills,
                job.skills,
            )

            role_score = cls.role_score(
                roles,
                job.job_title,
            )

            location_score = cls.location_score(
                location,
                job.location,
            )

            experience_score = cls.experience_score(
                experience,
                job.experience,
            )

            workmode_score = cls.workmode_score(
                work_modes,
                job.work_mode,
            )

            final_score = (

                skill_score * cls.SKILL_WEIGHT +

                role_score * cls.ROLE_WEIGHT +

                location_score * cls.LOCATION_WEIGHT +

                experience_score * cls.EXPERIENCE_WEIGHT +

                workmode_score * cls.WORKMODE_WEIGHT

            ) / 100

            job.match_score = round(
                final_score,
                2,
            )

            job.match_reason = cls.build_reason(

                skill_score,

                role_score,

                location_score,

                experience_score,

                workmode_score,

            )

        jobs.sort(

            key=lambda job: job.match_score,

            reverse=True,

        )

        return jobs

    @staticmethod
    def skill_score(
        resume: list[str],
        job: list[str],
    ) -> float:

        if not job:
            return 0

        resume = {

            s.lower().strip()

            for s in resume

        }

        matched = 0

        for skill in job:

            skill = skill.lower()

            if any(

                resume_skill in skill

                or skill in resume_skill

                for resume_skill in resume

            ):

                matched += 1

        return (matched / len(job)) * 100

    @staticmethod
    def role_score(
        roles: list[str],
        title: str,
    ) -> float:

        title = title.lower()

        for role in roles:

            role = role.lower()

            if role in title:

                return 100

        return 0

    @staticmethod
    def location_score(
        preferred: str,
        actual: str,
    ) -> float:

        if not preferred:

            return 100

        preferred = preferred.lower()

        actual = actual.lower()

        if preferred in actual:

            return 100

        if "remote" in actual:

            return 90

        if "hybrid" in actual:

            return 70

        return 0

    @staticmethod
    def experience_score(
        candidate: str,
        job: str,
    ) -> float:

        if not candidate:

            return 100

        if not job:

            return 80

        candidate_year = RankingService.extract_year(
            candidate
        )

        job_year = RankingService.extract_year(
            job
        )

        if candidate_year >= job_year:

            return 100

        if abs(candidate_year - job_year) <= 1:

            return 80

        return 40

    @staticmethod
    def extract_year(
        text: str,
    ) -> int:

        match = re.search(
            r"\d+",
            text,
        )

        if not match:

            return 0

        return int(match.group())

    @staticmethod
    def workmode_score(
        preferred: list[str],
        actual: str,
    ) -> float:

        if not preferred:

            return 100

        actual = actual.lower()

        for mode in preferred:

            if mode.lower() == actual:

                return 100

        return 50

    @staticmethod
    def build_reason(
        skill,
        role,
        location,
        experience,
        workmode,
    ) -> str:

        reasons = []

        if skill >= 80:
            reasons.append("Excellent skill match")

        elif skill >= 50:
            reasons.append("Good skill match")

        if role == 100:
            reasons.append("Relevant role")

        if location >= 90:
            reasons.append("Preferred location")

        if experience >= 80:
            reasons.append("Experience aligned")

        if workmode == 100:
            reasons.append("Preferred work mode")

        return ", ".join(reasons)