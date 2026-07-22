# apps/interview/services/gemini_service.py
import os
from google import genai
from google.genai import types

from apps.interview.expections import InterviewException


class GeminiService:
    """
    Service responsible only for communicating with Gemini.

    Input:
        Prompt

    Output:
        Raw text response
    """

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = os.getenv("GEMINI_MODEL")

    def _generate(self, prompt: str) -> str:
        """
        Internal method that sends a prompt to Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=4096,
                ),
            )

            return response.text.strip()

        except Exception as exc:
            raise InterviewException(
                f"Gemini API Error: {str(exc)}"
            ) from exc

    # ---------- Business Methods ----------

    def build_candidate_profile(self, prompt: str) -> str:
        return self._generate(prompt)

    def generate_question(self, prompt: str) -> str:
        return self._generate(prompt)

    def evaluate_answer(self, prompt: str) -> str:
        return self._generate(prompt)

    def generate_report(self, prompt: str) -> str:
        return self._generate(prompt)