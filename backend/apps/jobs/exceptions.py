class JobProviderException(Exception):
    """
    Raised when job provider fails.
    """
    pass


class InvalidJobProviderException(Exception):
    """
    Raised when provider is not supported.
    """
    pass