class AIProviderException(Exception):
    """
    Raised when AI provider fails.
    """
    pass


class InvalidProviderException(Exception):
    """
    Raised when provider is not supported.
    """
    pass


class AIResponseException(Exception):
    """
    Raised when provider returns invalid response.
    """
    pass