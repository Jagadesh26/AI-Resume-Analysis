import logging
import re

from apps.jobs.providers.base_provider import BaseJobProvider
from apps.jobs.services.normalization_service import NormalizationService


logger = logging.getLogger(__name__)


class RemoteOKProvider(BaseJobProvider):
    """
    RemoteOK Job Provider
    """

    BASE_URL = "https://remoteok.com/api"
    MIN_MATCH_SCORE = 2
    IGNORED_ROLE_TERMS = {
        "developer",
        "engineer",
        "full",
        "stack",
        "backend",
        "front",
        "end",
        "remote",
    }

    def search_jobs(
        self,
        *,
        role: str,
        location: str = "",
        skills: list[str] | None = None,
    ) -> list:

        logger.info(
            "Searching RemoteOK jobs for role=%s",
            role,
        )

        data = self.get(
            url=self.BASE_URL,
            headers={
                "Accept": "application/json"
            },
        )

        jobs = []

        if not isinstance(data, list):
            return jobs

        role_terms = self._terms_from_text(
            role,
            ignored=self.IGNORED_ROLE_TERMS,
        )
        skill_terms = {
            term
            for skill in skills or []
            for term in self._terms_from_text(skill)
        }

        # First element contains metadata
        for item in data[1:]:

            if not self._matches_job(
                item,
                role=role,
                role_terms=role_terms,
                skill_terms=skill_terms,
            ):
                continue

            jobs.append(
                NormalizationService.normalize_remoteok(
                    item
                )
            )

        return jobs

    @classmethod
    def _matches_job(
        cls,
        job: dict,
        *,
        role: str,
        role_terms: set[str],
        skill_terms: set[str],
    ) -> bool:

        position = (
            job.get("position") or ""
        ).lower()
        tags = {
            tag.lower()
            for tag in job.get("tags", [])
        }
        searchable_text = " ".join(
            [
                position,
                " ".join(tags),
                (job.get("description") or "").lower(),
            ]
        )

        if role.lower() in position:
            return True

        score = 0

        score += sum(
            1
            for term in role_terms
            if term in searchable_text
        )

        score += sum(
            1
            for term in skill_terms
            if term in tags or term in position
        )

        return score >= cls.MIN_MATCH_SCORE

    @staticmethod
    def _terms_from_text(
        text: str,
        *,
        ignored: set[str] | None = None,
    ) -> set[str]:

        ignored = ignored or set()

        return {
            term
            for term in re.findall(
                r"[a-z0-9]+",
                text.lower(),
            )
            if len(term) > 1 and term not in ignored
        }
