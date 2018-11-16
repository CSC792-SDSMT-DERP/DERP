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

    def __init__(self, session_action_type, data):
        self.__action_type = session_action_type
        self.__data = data

    def get_type(self):
        return self.__action_type

    def get_data(self):
        return self.__data


class SessionActionType(Enum):
    QUERY = 1
    LOAD_MODULE = 2         # data is a string containing the name of the module
    UNLOAD_MODULE = 3       # data is a string containing the name of the module
