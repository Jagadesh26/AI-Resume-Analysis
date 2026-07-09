from unittest.mock import patch

from django.test import SimpleTestCase

from apps.ai.exceptions import AIProviderException
from apps.ai.providers.openai_provider import OpenAIProvider
from apps.ai.services.analysis_service import AnalysisService


class OpenAIProviderTests(SimpleTestCase):
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}, clear=False)
    @patch("apps.ai.providers.openai_provider.OpenAI")
    def test_analyze_surfaces_quota_error(self, mock_openai_cls):
        mock_client = mock_openai_cls.return_value
        mock_client.responses.create.side_effect = Exception(
            "You exceeded your current quota"
        )

        provider = OpenAIProvider()

        with self.assertRaises(AIProviderException) as context:
            provider.analyze("hello")

        self.assertIn("quota", str(context.exception).lower())
        self.assertIn("billing", str(context.exception).lower())


class AnalysisServiceTests(SimpleTestCase):
    @patch("apps.ai.services.analysis_service.ResponseParser.parse")
    @patch("apps.ai.services.analysis_service.PromptBuilder.build_resume_analysis_prompt")
    @patch("apps.ai.services.analysis_service.ProviderFactory.get_provider")
    def test_analyze_resume_accepts_string_provider_response(
        self,
        mock_get_provider,
        mock_build_prompt,
        mock_parse,
    ):
        class DummyProvider:
            def analyze(self, prompt):
                return "raw response"

        mock_build_prompt.return_value = "prompt"
        mock_parse.return_value = {"summary": "ok"}
        mock_get_provider.return_value = DummyProvider()

        result = AnalysisService.analyze_resume(
            provider_name="groq",
            resume_text="resume text",
            target_role="engineer",
        )

        self.assertEqual(
            result["analysis"],
            {
                "summary": "ok",
                "recommended_jobs": [],
            },
        )
        mock_parse.assert_called_once_with("raw response")


class OutputSchemaTests(SimpleTestCase):
    def test_output_schema_includes_recommended_jobs(self):
        from apps.ai.prompts.output_schema import OutputSchema

        schema = OutputSchema.schema()

        self.assertIn("recommended_jobs", schema)
        self.assertEqual(schema["recommended_jobs"], [])
