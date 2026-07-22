from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models import User


class AuthenticationAPITests(APITestCase):
    def test_register_creates_user_and_returns_token(self):
        response = self.client.post(
            reverse("auth-register"),
            {
                "email": "test@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertIn("token", response.data["data"])
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_returns_existing_token(self):
        User.objects.create_user(
            email="login@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("auth-login"),
            {
                "email": "login@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["token_type"], "Bearer")

    def test_me_requires_authentication(self):
        response = self.client.get(reverse("auth-me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
