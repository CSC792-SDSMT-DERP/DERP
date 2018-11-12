"""
SessionAction.py

Class definition for the SessionAction object.
"""
from enum import Enum


class SessionAction:
    """
    A SessionAction defines a command to the SessionController, which may include sending a UXAction to the Repl, or
    performing a query.
    """

    def __init__(self, session_action_type, text=None, file_name=None, warnings=None):
        self.__action_type = session_action_type
        self.__file_name = file_name
        self.__warnings = warnings
        self.__text = text

    def get_type(self):
        return self.__action_type

    def get_file_name(self):
        return self.__file_name

    def get_warnings(self):
        return self.__warnings

    def get_text(self):
        return self.__text


class SessionActionType(Enum):
    QUERY = 1
    LOAD_MODULE = 2
    UNLOAD_MODULE = 3
