from typing import Any

from apps.ai.exceptions import AIResponseException


class ResponseValidator:
    """
    Validates AI response structure.
    """

    REQUIRED_KEYS = (
        "overall_score",
        "summary",
        "strengths",
        "weaknesses",
        "detected_skills",
        "missing_skills",
        "grammar",
        "formatting",
        "section_scores",
        "keyword_analysis",
        "achievement_suggestions",
        "resume_rewrites",
        "recommendations",
        "role_match",
        "recruiter_feedback",
        "recommended_jobs",
    )

    REQUIRED_TYPES = {
        "overall_score": dict,
        "summary": str,
        "strengths": list,
        "weaknesses": list,
        "detected_skills": list,
        "missing_skills": list,
        "grammar": dict,
        "formatting": dict,
        "section_scores": dict,
        "keyword_analysis": dict,
        "achievement_suggestions": list,
        "resume_rewrites": list,
        "recommendations": list,
        "role_match": list,
        "recruiter_feedback": dict,
        "recommended_jobs": list,
    }

    @classmethod
    def validate(cls, response: dict[str, Any]) -> dict[str, Any]:
        """
        Validate required response keys.
        """

        if not isinstance(response, dict):
            raise AIResponseException(
                "AI response must be a JSON object."
            )

        missing_keys = [
            key
            for key in cls.REQUIRED_KEYS
            if key not in response
        ]

        if missing_keys:
            raise AIResponseException(
                "Missing required response fields: "
                + ", ".join(missing_keys)
            )

        invalid_types = [
            key
            for key, expected_type in cls.REQUIRED_TYPES.items()
            if not isinstance(response.get(key), expected_type)
        ]

        if invalid_types:
            raise AIResponseException(
                "Invalid response field types: "
                + ", ".join(invalid_types)
            )

        score = response["overall_score"].get("score")

        if not isinstance(score, int) or not 0 <= score <= 100:
            raise AIResponseException(
                "overall_score.score must be an integer from 0 to 100."
            )

        return response
