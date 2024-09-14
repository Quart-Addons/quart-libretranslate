"""
quart_libretranslate.error
"""


class ApiError(Exception):
    """
    Custom exception for when receiving errors from LibreTranslate
    API.

    Arguments:
        message: The error message.
        code: The error code.
    """
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"{self.message} (Error Code: {self.code})"
