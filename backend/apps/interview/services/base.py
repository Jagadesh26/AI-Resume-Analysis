from abc import ABC, abstractmethod


class BaseResumeExtractor(ABC):

    @abstractmethod
    def extract(self, file_path: str) -> str:
        """Return extracted plain text."""
        pass