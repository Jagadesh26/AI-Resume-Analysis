import json
import re
from typing import Any

from apps.ai.exceptions import AIResponseException
from apps.ai.parsers.response_validator import ResponseValidator



class ResponseParser:
    """
    Parses and validates AI responses.

    Responsibilities:
    1. Clean AI response
    2. Extract JSON
    3. Convert JSON -> dict
    4. Validate schema
    """

    @classmethod
    def parse(cls, response: str) -> dict[str, Any]:
        """
        Parse raw AI response into validated dictionary.
        """

        if not response:
            raise AIResponseException(
                "Empty response received from AI provider."
            )

        cleaned_response = cls._clean_response(response)

        json_string = cls._extract_json(cleaned_response)

        try:
            parsed_response = json.loads(json_string)

        except json.JSONDecodeError as exc:
            raise AIResponseException(
                "AI provider returned invalid JSON."
            ) from exc

        return ResponseValidator.validate(parsed_response)

    @staticmethod
    def _clean_response(response: str) -> str:
        """
        Remove markdown formatting and whitespace.
        """

        response = response.strip()

        # Remove ```json
        response = re.sub(
            r"^```json\s*",
            "",
            response,
            flags=re.IGNORECASE,
        )

        # Remove ```
        response = re.sub(
            r"^```\s*",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"\s*```$",
            "",
            response,
        )

        return response.strip()

    @staticmethod
    def _extract_json(response: str) -> str:
        """
        Extract first JSON object from AI response.
        """

        start_index = response.find("{")
        end_index = response.rfind("}")

        if start_index == -1 or end_index == -1:
            raise AIResponseException(
                "No JSON object found in AI response."
            )

        return response[start_index : end_index + 1]