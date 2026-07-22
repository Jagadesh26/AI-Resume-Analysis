from django.contrib.auth import login
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.common.responses import ApiResponse


def build_auth_payload(user, token):
    refresh = RefreshToken.for_user(user)
    return {
        "token": token.key,
        "token_type": "Bearer",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
    }


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return ApiResponse.success(
            message="Registration successful.",
            data=build_auth_payload(user, token),
            status_code=status.HTTP_201_CREATED,
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Use the same token system as registration (DRF TokenAuthentication)
        token, _ = Token.objects.get_or_create(user=user)

        login(request, user)

        return ApiResponse.success(
            message="Login successful.",
            data=build_auth_payload(user, token),
        )
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()

        return ApiResponse.success(
                message="Logout successful.",
                data=None,
            )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ApiResponse.success(
            message="User profile fetched successfully.",
            data=UserSerializer(request.user).data,
        )
