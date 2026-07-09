from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Abstract base class for all resume extractors.
    """

    @abstractmethod
    def extract_text(self, file) -> str:
        """
        Extract text from uploaded file.
        """
        pass