"""DataGym exception classes.
Includes two main exceptions: :class:`.APIException` for when something goes
wrong on the server side, and :class:`.ClientException` when something goes
wrong on the client side. Both of these classes extend
:class:`.DatagymException`.
All other exceptions are subclassed from :class:`.ClientException`.
"""


class DatagymException(Exception):
    """The base DataGym Exception that all other exception classes extend."""


class APIException(DatagymException):
    """Indicate exception that involve responses from DataGyms's API."""

    def __init__(self, status: int, error: str, message: str, timestamp: int, path: str):
        """Initialize an instance of APIException.
        :param status: The status code set on DataGym's end.
        :param error: The error type set on DataGym's end.
        :param message: The associated message for the error.
        :param timestamp: The associated time when the error occurred.
        :param message: The associated api endpoint for the error.
        """
        error_str = "{} {}: '{}'".format(status, error, message)

        super().__init__(error_str)
        self.status = status
        self.error = error
        self.message = message
        self.timestamp = timestamp
        self.path = path


class ClientException(DatagymException):
    """Indicate exceptions that don't involve interaction with Reddit's API."""


class MissingRequiredAttributeException(ClientException):
    """Indicate exceptions caused by not including a required attribute."""
