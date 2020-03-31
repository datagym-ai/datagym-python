"""DataGym exception classes.

Includes two main exceptions: :class:`.APIException` for server side
exceptions, and :class:`.ClientException` when something goes wrong
on the client side. Both of these classes extend
:class:`.DatagymException`.

"""
from typing import List
import json
import re
from pkg_resources import resource_string, ResolutionError


class ExceptionMessageBuilder:
    """ The ExceptionMessageBuilder builds human-readable error messages

    The ExceptionMessageBuilder takes DataGym API error messages and
    converts them into a human-readable output for the User. Therefore,
    it needs the error values from the 'en.json' file.

    """
    FILE: str = "en.json"

    def __init__(self):
        """Initializes DataGym Client instance"""
        try:
            # Use pkg_resources to support Windows and Unix file paths
            # and find relative module path for file
            file_to_open = resource_string(__name__, self.FILE)
            self.errors = json.loads(file_to_open)

        except ResolutionError as e:
            print(e)
            self.errors = dict()

    def built_error_message(self, key: str, params: List[str]) -> str:
        """ Built the error Message from a key with specific params

        :param str key: A error key that links to a error msg template
        :param List[str] params: Parameters for filling the msg template
        :returns: Human-readable error message
        :rtype: str
        """
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
                 details: List = None,
                 **kwargs):
        """ Initializes APIException instance

        :param ExceptionMessageBuilder msg_builder: Error message converter
        :param int status_code: HTTP status code
        :param str key: Error key from DataGym API
        :param List[str] params: Error Values for error message template
        :param str msg: Error message provided by DataGym API
        :param int code: HTTP status code
        :param List details: Error details from the DataGym API
        """
        if "error" in kwargs and "path" in kwargs and "message" in kwargs:
            error_str = "{} | Message: {} | Endpoint: {}".format(kwargs["error"],
                                                                 kwargs["message"],
                                                                 kwargs["path"])
        else:
            code = status_code if status_code else code
            error_msg = msg_builder.built_error_message(key, params)
            error_msg = msg if msg and not error_msg else error_msg
            error_str = f'HTTP {code} | Message: "{error_msg}"'

        super().__init__(error_str)


class ClientException(DatagymException):
    """Indicate exceptions that involve wrong input from the user."""

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
        """ Initializes ClientException instance

        :param ExceptionMessageBuilder msg_builder: Error message converter
        :param int status_code: HTTP status code
        :param str error: Error message provided by DataGym API
        :param int message: Error message provided by DataGym API
        :param int timestamp: Timestamp when Error occurred
        :param str path: API path where error occurred
        :param int status_code: HTTP status code
        :param str key: Error key from DataGym API
        :param List[str] params: Error Values for error message template
        :param str msg: Error message provided by DataGym API
        :param int code: HTTP status code
        :param List details: Error details from the DataGym API
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
        """ Initializes InvalidTokenException instance

        :param args:
        """
        super().__init__(**args)
