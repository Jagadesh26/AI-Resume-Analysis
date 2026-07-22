from rest_framework import serializers

from apps.resumes.validators import validate_resume_file


class ResumeAnalyzeSerializer(serializers.Serializer):
    """
    Serializer for Resume Analysis API
    """

    PROVIDER_CHOICES = (
        ("gemini", "Gemini"),
        ("groq", "Groq"),
        ("openrouter", "OpenRouter"),
        ("openai", "OpenAI"),
        ("claude", "Claude"),
        ("gpt-oss", "GPT-OSS"),
        ("qwen", "Qwen"),
    )

    resume = serializers.FileField(
        required=True,
        allow_empty_file=False,
    )

    provider = serializers.ChoiceField(
        choices=PROVIDER_CHOICES,
        required=True,
    )

    target_role = serializers.CharField(
        required=True,
        max_length=150,
        trim_whitespace=True,
    )

    def validate_resume(self, value):
        """
        Validate uploaded resume file.
        """
        validate_resume_file(value)
        return value

    def validate_target_role(self, value):
        """
        Validate target role.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Target role is required."
            )

        return value