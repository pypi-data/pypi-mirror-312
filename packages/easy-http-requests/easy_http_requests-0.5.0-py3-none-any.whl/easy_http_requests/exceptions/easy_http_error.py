from typing import Optional


class EasyHttpRequestError(Exception):
    """General exception for EasyHttpRequest errors."""

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception


class EasyHttpTimeoutError(EasyHttpRequestError):
    """Exception raised for request timeouts."""

    pass


class EasyHttpConnectionError(EasyHttpRequestError):
    """Exception raised for connection errors."""

    pass
