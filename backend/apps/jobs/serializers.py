from rest_framework import serializers

from apps.jobs.constant import DEFAULT_JOB_LIMIT


class JobSearchSerializer(serializers.Serializer):
    """
    Serializer for job search requests.
    """

    roles = serializers.ListField(
        child=serializers.CharField(
            max_length=150,
            trim_whitespace=True,
        ),
        allow_empty=False,
        required=False,
    )

    preferred_location = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
        trim_whitespace=True,
        default="",
    )

    skills = serializers.ListField(
        child=serializers.CharField(
            max_length=100,
            trim_whitespace=True,
        ),
        required=False,
        default=list,
    )

    experience_level = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        trim_whitespace=True,
        default="",
    )

    work_modes = serializers.ListField(
        child=serializers.CharField(
            max_length=50,
            trim_whitespace=True,
        ),
        required=False,
        default=list,
    )

    limit = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=50,
        default=DEFAULT_JOB_LIMIT,
    )

    def validate_roles(self, value):
        roles = [
            role.strip()
            for role in value
            if role.strip()
        ]

        if not roles:
            raise serializers.ValidationError(
                "At least one role is required."
            )

        return roles
