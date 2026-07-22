


# apps/interview/choices.py

from django.db import models


class InterviewType(models.TextChoices):
    TECHNICAL = "technical", "Technical"
    HR = "hr", "HR"
    MIXED = "mixed", "Mixed"
    BACKEND = "Backend", "Backend"
    FRONTEND = "Frontend", "Frontend"
    FULL_STACK = "Full Stack", "Full Stack"
    DATA_ENGINEER = "Data Engineer", "Data Engineer"


class InterviewLevel(models.TextChoices):
    FRESHER = "fresher", "Fresher"
    JUNIOR = "junior", "Junior"
    JUNIOR_TITLE = "Junior", "Junior"
    MID = "mid", "Mid-Level"
    MID_TITLE = "Mid", "Mid"
    SENIOR = "senior", "Senior"
    SENIOR_TITLE = "Senior", "Senior"


class DifficultyLevel(models.TextChoices):
    EASY = "easy", "Easy"
    EASY_TITLE = "Easy", "Easy"
    MEDIUM = "medium", "Medium"
    MEDIUM_TITLE = "Medium", "Medium"
    HARD = "hard", "Hard"
    HARD_TITLE = "Hard", "Hard"


class InterviewStatus(models.TextChoices):
    CREATED = "created", "Created"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"
