from docx import Document
import pdfplumber

from .base import BaseResumeExtractor


class PDFResumeExtractor(BaseResumeExtractor):

    def extract(self, file_path) -> str:
        text = []

        if hasattr(file_path, "seek"):
            file_path.seek(0)

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text)
    






class DOCXResumeExtractor(BaseResumeExtractor):

    def extract(self, file_path) -> str:

        if hasattr(file_path, "seek"):
            file_path.seek(0)

        doc = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )
