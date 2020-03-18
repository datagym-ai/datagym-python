"""DataGym exception classes.
Includes two main exceptions: :class:`.APIException` for when something goes
wrong on the server side, and :class:`.ClientException` when something goes
wrong on the client side. Both of these classes extend
:class:`.DatagymException`.
All other exceptions are subclassed from :class:`.ClientException`.
"""
from typing import List


class DatagymException(Exception):
    """The base DataGym Exception that all other exception classes extend."""


class APIException(DatagymException):
    """Indicate exception that involve responses from DataGyms's API."""
    def __init__(self,
                 status_code: int = None,
                 key: str = None,
                 params: List[str] = None,
                 msg: str = None,
                 code: int = None,
                 details: List = None):

        code = status_code if status_code else code

        error_str = ''' 
                        HTTP {} 
                        key = {}, 
                        msg = {}, 
                        params = {}
                        details = {}
                    '''.format(code, key, msg, ", ".join(params), ", ".join(details))
        super().__init__(error_str)


class ClientException(DatagymException):
    """Indicate exceptions that don't involve interaction with Reddit's API."""

    def __init__(self,
                 status_code: int = None,
                 status: int = None,
                 error: str = None,
                 message: str = None,
                 timestamp: int = None,
                 path: str= None):
        """Initialize an instance of APIException.
        :param status: The status code set on DataGym's end.
        :param error: The error type set on DataGym's end.
        :param message: The associated message for the error.
        :param timestamp: The associated time when the error occurred.
        :param message: The associated api endpoint for the error.
        """
        status = status_code if status_code else status
        error_str = "{} {}: '{}'".format(status, error, message)

        super().__init__(error_str)
        self.status = status
        self.error = error
        self.message = message
        self.timestamp = timestamp
        self.path = path


class InvalidTokenException(ClientException):
    """Indicate exceptions caused by invalid token."""
    def __init__(self):
        error_str = "Invalid Token"
        super().__init__(error_str)


class MissingRequiredAttributeException(ClientException):
    """Indicate exceptions caused by not including a required attribute."""
