from docx import Document

from apps.resumes.extractors.base_extractor import BaseExtractor


class DOCXExtractor(BaseExtractor):

    def extract_text(self, file) -> str:

        document = Document(file)

        extracted_text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                extracted_text.append(
                    paragraph.text.strip()
                )

        return "\n".join(extracted_text)