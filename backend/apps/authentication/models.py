import uuid

from django.contrib.auth.models import (
    AbstractUser,
)

from django.db import models


from apps.authentication.managers import UserManager


class User(
    AbstractUser,
):

    username = None

    first_name = None

    last_name = None

    date_joined = None

    id = models.UUIDField(

        primary_key=True,

        default=uuid.uuid4,

        editable=False,

    )

    email = models.EmailField(

        unique=True,

        db_index=True,

    )

    is_email_verified = models.BooleanField(

        db_column="is_verified",

        default=False,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:

        db_table = "users"

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.email
