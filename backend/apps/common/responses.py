from typing import Any, Dict, Optional

from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    """
    Standard API Response Format

    Success:
    {
        "success": true,
        "message": "...",
        "data": {}
    }

    Error:
    {
        "success": false,
        "message": "...",
        "errors": {}
    }
    """

    @staticmethod
    def success(
        *,
        message: str,
        data: Optional[Any] = None,
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def error(
        *,
        message: str,
        errors: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors,
            },
            status=status_code,
        )