from rest_framework import serializers

from apps.interview.models import InterviewReport, InterviewSession


class InterviewUploadSerializer(serializers.Serializer):
    resume = serializers.FileField()

    interview_type = serializers.ChoiceField(
        choices=[
            ("Backend", "Backend"),
            ("Frontend", "Frontend"),
            ("Full Stack", "Full Stack"),
            ("Data Engineer", "Data Engineer"),
        ]
    )

    interview_level = serializers.ChoiceField(
        choices=[
            ("Junior", "Junior"),
            ("Mid", "Mid"),
            ("Senior", "Senior"),
        ]
    )

    difficulty = serializers.ChoiceField(
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
        ]
    )

    total_questions = serializers.IntegerField(
        min_value=1,
        max_value=20,
    )

    def validate_resume(self, file):

        allowed_extensions = {
            "pdf",
            "docx",
        }

        extension = file.name.split(".")[-1].lower()

        if extension not in allowed_extensions:

            raise serializers.ValidationError(
                "Only PDF and DOCX are supported."
            )

        max_size = 5 * 1024 * 1024

        if file.size > max_size:

            raise serializers.ValidationError(
                "Resume cannot exceed 5MB."
            )

        return file
    





class InterviewReportSerializer(serializers.ModelSerializer):

    class Meta:

        model = InterviewReport

        fields = (
            "overall_score",
            "report_json",
            "created_at",
        )





class InterviewHistorySerializer(serializers.ModelSerializer):

    session_id = serializers.UUIDField(
        source="id",
        read_only=True
    )

    overall_score = serializers.SerializerMethodField()

    class Meta:

        model = InterviewSession

        fields = (
            "session_id",
            "interview_type",
            "interview_level",
            "difficulty",
            "status",
            "overall_score",
            "started_at",
            "completed_at",
        )

    def get_overall_score(self, obj):

        if hasattr(obj, "interview_report"):
            return obj.interview_report.overall_score

        return None
    




class InterviewDetailSerializer(serializers.ModelSerializer):

    session_id = serializers.UUIDField(
        source="id",
        read_only=True,
    )

    overall_score = serializers.SerializerMethodField()

    has_report = serializers.SerializerMethodField()

    class Meta:

        model = InterviewSession

        fields = (
            "session_id",
            "interview_type",
            "interview_level",
            "difficulty",
            "status",
            "total_questions",
            "started_at",
            "completed_at",
            "overall_score",
            "has_report",
        )

    def get_overall_score(self, obj):

        if hasattr(obj, "interview_report"):
            return obj.interview_report.overall_score

        return None

    def get_has_report(self, obj):

        return hasattr(obj, "interview_report")
