# apps/interview/services/profile_builder.py

from apps.interview.prompts.resume_profile_prompt import PROFILE_BUILDER_PROMPT
from apps.interview.gemini_provider import GeminiService
from apps.interview.services.json_validator import JsonValidator
from apps.interview.expections import AIResponseValidationError




class ProfileBuilder:
    """
    Builds a structured candidate profile
    from raw resume text.
    """

    def __init__(self):
        self.gemini_service = GeminiService()

    def build(self, raw_resume_text: str) -> dict:
        """
        Build candidate profile from resume.
        """

        if not raw_resume_text:
            raise AIResponseValidationError(
                "Resume text cannot be empty."
            )

        prompt = PROFILE_BUILDER_PROMPT.format(resume_text=raw_resume_text)

        response = self.gemini_service.build_candidate_profile(prompt)

        profile = JsonValidator.parse(response)

        self._validate_profile(profile)

        return profile

    def _validate_profile(self, profile: dict) -> None:
        """
        Validate required fields returned by Gemini.
        """

        required_fields = [
            "candidate",
            "skills",
            "experience",
            "education",
            "projects",
        ]

        missing = [
            field
            for field in required_fields
            if field not in profile
        ]

        if missing:
            raise AIResponseValidationError(
                f"Missing required fields: {', '.join(missing)}"
            )