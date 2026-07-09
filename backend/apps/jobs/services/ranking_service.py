import re

from apps.jobs.schemas.job_schema import JobSchema


class RankingService:
    """
    Ranks jobs based on resume data.
    """

    SKILL_WEIGHT = 0.50
    ROLE_WEIGHT = 0.25
    LOCATION_WEIGHT = 0.15
    EXPERIENCE_WEIGHT = 0.05
    WORK_MODE_WEIGHT = 0.05

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

        ranked_jobs = []

        for job in jobs:

            skill_score = cls._calculate_skill_score(
                skills,
                job.skills,
            )

            role_score = cls._calculate_role_score(
                roles,
                job.job_title,
            )

            location_score = cls._calculate_location_score(
                location,
                job.location,
            )

            experience_score = cls._calculate_experience_score(
                experience,
                job.experience,
            )

            work_mode_score = cls._calculate_work_mode_score(
                work_modes,
                job.work_mode,
            )

            final_score = (

                skill_score * cls.SKILL_WEIGHT +

                role_score * cls.ROLE_WEIGHT +

                location_score * cls.LOCATION_WEIGHT +

                experience_score * cls.EXPERIENCE_WEIGHT +

                work_mode_score * cls.WORK_MODE_WEIGHT

            )

            job.match_score = round(
                final_score,
                2,
            )

            job.match_reason = cls._build_reason(
                skill_score,
                role_score,
                location_score,
            )

            ranked_jobs.append(job)

        ranked_jobs.sort(
            key=lambda x: x.match_score,
            reverse=True,
        )

        return ranked_jobs

    @staticmethod
    def _calculate_skill_score(
        resume_skills: list[str],
        job_skills: list[str],
    ) -> float:

        if not job_skills:
            return 0

        resume = {
            skill.lower()
            for skill in resume_skills
        }

        job = {
            skill.lower()
            for skill in job_skills
        }

        matched = resume.intersection(job)

        return (
            len(matched) / len(job)
        ) * 100

    @staticmethod
    def _calculate_role_score(
        roles: list[str],
        job_title: str,
    ) -> float:

        job_title = job_title.lower()

        for role in roles:

            if role.lower() in job_title:
                return 100

        return 0

    @staticmethod
    def _calculate_location_score(
        preferred_location: str,
        job_location: str,
    ) -> float:

        if not preferred_location:
            return 100

        if preferred_location.lower() in job_location.lower():
            return 100

        if "remote" in job_location.lower():
            return 90

        return 0

    @staticmethod
    def _calculate_experience_score(
        candidate: str,
        job: str,
    ) -> float:

        if not candidate:
            return 100

        if not job:
            return 80

        if candidate.lower() == job.lower():
            return 100

        return 70

    @staticmethod
    def _calculate_work_mode_score(
        preferred_modes: list[str],
        job_mode: str,
    ) -> float:

        if not preferred_modes:
            return 100

        for mode in preferred_modes:

            if mode.lower() == job_mode.lower():
                return 100

        return 50

    @staticmethod
    def _build_reason(
        skill_score: float,
        role_score: float,
        location_score: float,
    ) -> str:

        reasons = []

        if skill_score >= 80:
            reasons.append("Excellent skill match.")

        elif skill_score >= 50:
            reasons.append("Good skill match.")

        else:
            reasons.append("Limited skill match.")

        if role_score == 100:
            reasons.append("Role matches your profile.")

        if location_score >= 90:
            reasons.append("Preferred location matches.")

        return " ".join(reasons)