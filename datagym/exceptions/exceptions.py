"""DataGym exception classes.
Includes two main exceptions: :class:`.APIException` for when something goes
wrong on the server side, and :class:`.ClientException` when something goes
wrong on the client side. Both of these classes extend
:class:`.DatagymException`.
All other exceptions are subclassed from :class:`.ClientException`.
"""
from typing import List
from pathlib import Path
import json
import re
from pkg_resources import resource_string, ResolutionError

class ExceptionMessageBuilder:
    FILE: str = "en.json"

    def __init__(self):
        try:
            # Use pkg_resources to support Windows and Unix file paths and find relative module path for file
            file_to_open = resource_string(__name__, self.FILE)
            self.errors = json.loads(file_to_open)

        except ResolutionError as e:
            self.errors = dict()

    def built_error_message(self, key: str, params: List[str]) -> str:
        if key in self.errors:
            error_msg = self.errors[key]
            error_msg = re.sub("{..}", "", error_msg)
            return error_msg.format(*params)
        else:
            return ""


class DatagymException(Exception):
    """The base DataGym Exception that all other exception classes extend."""


class APIException(DatagymException):
    """Indicate exception that involve responses from DataGyms's API."""

    def __init__(self,
                 msg_builder: ExceptionMessageBuilder,
                 status_code: int = None,
                 key: str = None,
                 params: List[str] = None,
                 msg: str = None,
                 code: int = None,
                 details: List = None):
        code = status_code if status_code else code
        error_msg = msg_builder.built_error_message(key, params)
        error_msg = msg if msg and not error_msg else error_msg
        error_str = f'HTTP {code} | Message: "{error_msg}"'
        super().__init__(error_str)


class ClientException(DatagymException):
    """Indicate exceptions that don't involve interaction with Reddit's API."""

    def __init__(self,
                 msg_builder: ExceptionMessageBuilder,
                 status_code: int = None,
                 status: int = None,
                 error: str = None,
                 message: str = None,
                 timestamp: int = None,
                 path: str = None,
                 key: str = None,
                 params: List[str] = None,
                 msg: str = None,
                 code: int = None,
                 details: List = None):
        """Initialize an instance of APIException.
        :param status: The status code set on DataGym's end.
        :param error: The error type set on DataGym's end.
        :param message: The associated message for the error.
        :param timestamp: The associated time when the error occurred.
        :param message: The associated api endpoint for the error.
        """
        if not code:
            code = status_code if status_code else status

        error_msg = msg_builder.built_error_message(key, params)
        error_msg = msg if msg and not error_msg else error_msg
        error_str = f'HTTP {code} | Message: "{error_msg}"'

        super().__init__(error_str)


class InvalidTokenException(ClientException):
    """Indicate exceptions caused by invalid token."""

    def __init__(self, **args):
        error_str = "Invalid Token"
        super().__init__(**args)
