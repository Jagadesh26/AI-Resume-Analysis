from pypdf import PdfReader

from apps.resumes.extractors.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):

    def extract_text(self, file) -> str:

        reader = PdfReader(file)

        extracted_text = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                extracted_text.append(text)

        return "\n".join(extracted_text).strip()