import logging

from apps.ai.parsers.response_parsers import ResponseParser
from apps.ai.prompts.prompt_builder import PromptBuilder
from apps.ai.providers.provider_factory import ProviderFactory
from apps.ai.providers.provider_response import AIProviderResponse


logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Coordinates the complete AI resume analysis workflow.

    Workflow:

    Resume
        ↓
    Prompt Builder
        ↓
    AI Provider
        ↓
    Response Parser
        ↓
    Job Search
        ↓
    Merge Response
    """

    @staticmethod
    def analyze_resume(
        *,
        provider_name: str,
        resume_text: str,
        target_role: str,
    ) -> dict:
        """
        Execute the complete resume analysis pipeline.
        """

        # ---------------------------------------------------------
        # Build AI Prompt
        # ---------------------------------------------------------

        prompt = PromptBuilder.build_resume_analysis_prompt(
            resume_text=resume_text,
            target_role=target_role,
        )

        # ---------------------------------------------------------
        # Select AI Provider
        # ---------------------------------------------------------

        provider = ProviderFactory.get_provider(
            provider_name
        )

        # ---------------------------------------------------------
        # Execute AI Analysis
        # ---------------------------------------------------------

        provider_response = provider.analyze(
            prompt
        )

        # Backward compatibility
        if isinstance(provider_response, str):

            provider_response = AIProviderResponse(
                provider=provider_name,
                model=getattr(provider, "model", ""),
                raw_text=provider_response,
                usage=None,
            )

        # ---------------------------------------------------------
        # Parse AI Response
        # ---------------------------------------------------------

        analysis = ResponseParser.parse(
            provider_response.raw_text
        )

        if not isinstance(analysis, dict):
            analysis = {}

        # ---------------------------------------------------------
        # Merge Job Recommendations
        # ---------------------------------------------------------

        analysis["recommended_jobs"] = []

        # ---------------------------------------------------------
        # Return Final Response
        # ---------------------------------------------------------

        return {

            "provider": provider_response.provider,

            "model": provider_response.model,

            "usage": provider_response.usage,

            "analysis": analysis,

        }
