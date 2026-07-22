# apps/interview/services/json_validator.py

import json
import re

from apps.interview.expections import AIResponseValidationError


class JsonValidator:
    """
    Validates and parses AI JSON responses.
    """

    @staticmethod
    def parse(response: str) -> dict:
        """
        Convert AI response into a Python dictionary.
        """

        if not response:
            raise AIResponseValidationError(
                "Empty AI response received."
            )

        cleaned = response.strip()

        # Remove markdown code fences
        cleaned = re.sub(
            r"^```json\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"^```",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned,
        )

        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)

        except json.JSONDecodeError as exc:
            raise AIResponseValidationError(
                f"Invalid JSON returned by Gemini: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise AIResponseValidationError(
                "AI response must be a JSON object."
            )

        return data