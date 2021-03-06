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

    def __init__(self, session_action_type, data, warnings=None):
        self.__action_type = session_action_type
        self.__data = data
        self.__warnings = warnings or list()

    def add_warning(self, warning):
        self.__warnings.append(warning)

    def get_type(self):
        return self.__action_type

    def get_data(self):
        return self.__data

    def get_warnings(self):
        return self.__warnings


class ModeChangeType(Enum):
    EXIT = 1
    # Exit the current mode

    SELECTION = 2
    # Switch to selection mode

    CRITERIA = 3
    # Switch to criteria mode


class SessionActionType(Enum):
    QUERY = 1
    # data : str if in Main Mode else None - name of selection execute

    LOAD_MODULE = 2
    # data : str - name of the module

    UNLOAD_MODULE = 3
    # data : str - name of the module

    RECALL = 4
    # data : str if in Main Mode else None - name of selection or criteria to recall

    CHANGE_MODE = 5
    # data : SessionActionModeType - Mode to change to

    SAVE_BUFFER = 6
    # data : str - Name to save the buffer under

    APPEND_TO_BUFFER = 7
    # data : None; indicates to add the line that generated the evaluated AST

    CLEAR_BUFFER = 8
    # data : None

    NOOP = 9
    # data : None
