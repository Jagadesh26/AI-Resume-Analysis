import os

from apps.resumes.extractors.pdf_extractor import PDFExtractor
from apps.resumes.extractors.docx_extractor import DOCXExtractor


class ExtractorFactory:

    @staticmethod
    def get_extractor(file):

        extension = os.path.splitext(
            file.name
        )[1].lower()

        if extension == ".pdf":

            return PDFExtractor()

        if extension == ".docx":

            return DOCXExtractor()

        raise ValueError(
            "Unsupported resume format."
        )