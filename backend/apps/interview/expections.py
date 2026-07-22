# apps/interview/exceptions.py

class InterviewException(Exception):
    """Base exception for interview module."""
    pass


class ResumeExtractionError(InterviewException):
    pass


class AIResponseValidationError(InterviewException):
    pass


class InterviewSessionError(InterviewException):
    pass


class InterviewCompletedError(InterviewException):
    pass


class UnsupportedResumeFormatError(InterviewException):
    pass