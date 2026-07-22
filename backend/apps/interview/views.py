from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from apps.authentication.authentication import BearerTokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.interview.serializers import (
    InterviewDetailSerializer,
    InterviewHistorySerializer,
    InterviewReportSerializer,
    InterviewUploadSerializer,
)
from apps.interview.services.interview_builder import InterviewService


class InterviewHistoryPagination(
    PageNumberPagination
):

    page_size = 10

    page_size_query_param = "page_size"

    max_page_size = 100


class InterviewUploadAPIView(APIView):
    # Ensure the view uses token based authentication. DRF's default
    # TokenAuthentication expects the header ``Authorization: Token <key>``.
    # The project also provides a custom ``BearerTokenAuthentication``
    # that accepts ``Bearer <key>``.  Adding both authentication classes
    # guarantees that the API accepts either style and prevents the
    # ``Invalid token`` error when a client sends a bearer token.
    authentication_classes = [
        TokenAuthentication,
        BearerTokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewUploadSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        service = InterviewService()

        result = service.start_interview(

            user=request.user,

            uploaded_file=serializer.validated_data["resume"],

            interview_type=serializer.validated_data["interview_type"],

            interview_level=serializer.validated_data["interview_level"],

            difficulty=serializer.validated_data["difficulty"],

            total_questions=serializer.validated_data["total_questions"],
        )

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )
    



class InterviewReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewReportSerializer

    def get(
        self,
        request,
        session_id,
    ):

        service = InterviewService()

        report = service.get_report(
            session_id=session_id,
            user=request.user,
        )

        serializer = self.serializer_class(
            report
        )

        return Response(
            serializer.data
        )
    



class InterviewHistoryAPIView(
    APIView
):
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewHistorySerializer

    pagination_class = (
        InterviewHistoryPagination
    )

    def get(self, request):

        service = InterviewService()

        queryset = service.get_history(
            user=request.user
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    





class InterviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = InterviewDetailSerializer

    def get(
        self,
        request,
        session_id,
    ):

        service = InterviewService()

        interview = service.get_interview(
            user=request.user,
            session_id=session_id,
        )

        serializer = self.serializer_class(
            interview
        )

        return Response(
            serializer.data
        )
