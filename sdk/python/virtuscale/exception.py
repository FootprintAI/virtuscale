from __future__ import annotations

from http import HTTPStatus

class VirtuscaleException(Exception):
    """
    Base class for Virtuscale's errors. Each custom exception should be derived from this class.
    """

    error_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class BadParamException(VirtuscaleException):
    """
    Raised when received invalid input arguments
    """
    error_code = HTTPStatus.BAD_REQUEST
