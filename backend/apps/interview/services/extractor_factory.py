from pathlib import Path

from .extractor import PDFResumeExtractor, DOCXResumeExtractor


class ResumeExtractorFactory:

    @staticmethod
    def get(file_obj):
        file_name = getattr(file_obj, "name", str(file_obj))
        return ResumeExtractorFactory.get_extractor(file_name)

    @staticmethod
    def get_extractor(file_name: str):

        extension = Path(file_name).suffix.lower()

        if extension == ".pdf":
            return PDFResumeExtractor()

        if extension == ".docx":
            return DOCXResumeExtractor()

        raise ValueError("Unsupported resume format")
