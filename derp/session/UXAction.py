"""
UXAction.py

Class definition for the UXAction object.
"""
from enum import Enum


class UXAction:
    """
    UXActions relay instructions from the SessionController to the Repl, and include
    warnings and text to output.

    Consists of the action for the UI to take and any data needed to carry out the action.
    UX actions are produced when the backend processes a line of input.
    As a result, any warnings encountered in the backend while preparing the data will be included in the UX action.
    """

    def __init__(self, action_type, data=None, warnings=None):
        self.__data = data
        self.__warnings = warnings or list()
        self.__type = action_type

    def get_warnings(self):
        return self.__warnings

    def get_data(self):
        return self.__data

    def get_type(self):
        return self.__type


class UXActionModeType(Enum):
    MAIN = 1
    # Switch to main mode

    SELECTION = 2
    # Switch to selection mode

    CRITERIA = 3
    # Switch to criteria mode


class UXActionType(Enum):
    """
    UXActionTypes indicate what type of action a UXAction is

    Possible Actions:
    Read - Present user with posts from a Post iterator/Selection executor
    Recall - Output text of a previously defined criteria or selection
    Error - Display error message
    Change Mode - Keep running as normal, enter the mode given in the action
    NOOP - Do nothing, continue as usual
    Exit - Close the REPL and end execution
    """
    READ = 0            # Data is a selection executor
    RECALL = 1          # Data is a list of strings
    ERROR = 2           # Data is an exception
    CHANGE_MODE = 3     # Data is a UXActionModeType
    NO_OP = 4           # Data is None
    EXIT = 5            # Data is None
