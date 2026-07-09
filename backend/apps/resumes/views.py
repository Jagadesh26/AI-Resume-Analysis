import logging

from rest_framework import status
from rest_framework.views import APIView

from apps.ai.exceptions import (
    AIProviderException,
    AIResponseException,
    InvalidProviderException,
)
from apps.ai.services.analysis_service import AnalysisService
from apps.common.responses import ApiResponse
from apps.resumes.services import ResumeExtractionService
from apps.resumes.serializers import ResumeAnalyzeSerializer


logger = logging.getLogger(__name__)


class ResumeAnalyzeAPIView(APIView):
    """
    Analyze uploaded resume using selected AI provider.
    """

    serializer_class = ResumeAnalyzeSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        if not serializer.is_valid():

            return ApiResponse.error(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        resume = serializer.validated_data["resume"]
        provider = serializer.validated_data["provider"]
        target_role = serializer.validated_data["target_role"]

        try:

            resume_text = (
                ResumeExtractionService.extract_resume_text(
                    resume
                )
            )

            analysis = (
                AnalysisService.analyze_resume(
                    provider_name=provider,
                    resume_text=resume_text,
                    target_role=target_role,
                )
            )

            return ApiResponse.success(
                message="Resume analyzed successfully.",
                data=analysis,
                status_code=status.HTTP_200_OK,
            )

        except (
            InvalidProviderException,
            AIProviderException,
            AIResponseException,
            ValueError,
        ) as exc:

            return ApiResponse.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as exc:
            logger.exception(
                "Unexpected resume analysis failure."
            )

            return ApiResponse.error(
                message="Internal Server Error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
