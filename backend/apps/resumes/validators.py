import os
from zipfile import is_zipfile

from rest_framework.serializers import ValidationError


ALLOWED_EXTENSIONS = {".pdf", ".docx"}

ALLOWED_CONTENT_TYPES = {
    ".pdf": {"application/pdf"},
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
    },
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_resume_file(file) -> None:
    """
    Validate uploaded resume.
    """

    if not file:
        raise ValidationError("Resume file is required.")

    if file.size == 0:
        raise ValidationError("Uploaded file is empty.")

    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            "Maximum allowed file size is 5 MB."
        )

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            "Only PDF and DOCX files are allowed."
        )

    content_type = getattr(file, "content_type", None)

    if (
        content_type
        and content_type not in ALLOWED_CONTENT_TYPES[extension]
    ):
        raise ValidationError(
            "Uploaded file type does not match its extension."
        )

    current_position = file.tell()
    file.seek(0)

    try:
        if extension == ".pdf":
            if file.read(5) != b"%PDF-":
                raise ValidationError(
                    "Uploaded PDF file is invalid."
                )

        if extension == ".docx" and not is_zipfile(file):
            raise ValidationError(
                "Uploaded DOCX file is invalid."
            )
    finally:
        file.seek(current_position)
