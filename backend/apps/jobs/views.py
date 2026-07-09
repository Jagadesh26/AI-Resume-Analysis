import logging
from dataclasses import asdict

from rest_framework import status
from rest_framework.views import APIView

from apps.common.responses import ApiResponse
from apps.jobs.exceptions import (
    InvalidJobProviderException,
    JobProviderException,
)
from apps.jobs.serializers import JobSearchSerializer
from apps.jobs.services.job_search_service import JobSearchService


logger = logging.getLogger(__name__)


class JobSearchAPIView(APIView):
    """
    Search jobs using normalized resume analysis data.
    """

    serializer_class = JobSearchSerializer

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

        data = serializer.validated_data

        try:

            jobs = JobSearchService.search_jobs(
                roles=data["roles"],
                preferred_location=data.get(
                    "preferred_location",
                    "",
                ),
                skills=data.get(
                    "skills",
                    [],
                ),
                experience_level=data.get(
                    "experience_level",
                    "",
                ),
                work_modes=data.get(
                    "work_modes",
                    [],
                ),
                limit=data.get(
                    "limit",
                    20,
                ),
            )

            return ApiResponse.success(
                message="Jobs fetched successfully.",
                data={
                    "recommended_jobs": [
                        asdict(job)
                        for job in jobs
                    ],
                },
                status_code=status.HTTP_200_OK,
            )

        except (
            InvalidJobProviderException,
            JobProviderException,
            ValueError,
        ) as exc:

            return ApiResponse.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception(
                "Unexpected job search failure."
            )

            return ApiResponse.error(
                message="Internal Server Error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
