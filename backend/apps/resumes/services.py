import re

from apps.resumes.extractors.extractor_factory import ExtractorFactory


class ResumeTextCleaner:
    """
    Cleans extracted resume text before
    sending it to the AI model.
    """

    @staticmethod
    def clean(text: str) -> str:

        if not text:
            return ""

        # Remove carriage returns
        text = text.replace("\r", "\n")

        # Remove tabs
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip each line
        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        # Remove empty lines
        lines = [
            line
            for line in lines
            if line
        ]

        return "\n".join(lines).strip()
    





class ResumeExtractionService:

    @staticmethod
    def extract_resume_text(file) -> str:
        try:
            extractor = ExtractorFactory.get_extractor(
                file
            )

            extracted_text = extractor.extract_text(
                file
            )
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(
                "Could not read the uploaded resume file."
            ) from exc

        cleaned_text = ResumeTextCleaner.clean(
            extracted_text
        )

        if not cleaned_text:
            raise ValueError(
                "No readable text found in the uploaded resume."
            )

        return cleaned_text
