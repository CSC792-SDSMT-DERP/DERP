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

    def __init__(self, action_type, data=None, warnings=[]):
        self.__data = data
        self.__warnings = warnings
        self.__type = action_type

    def get_warnings(self):
        return self.__warnings

    def get_data(self):
        return self.__data

    def get_type(self):
        return self.__type


class UXActionType(Enum):
    """
    UXActionTypes indicate what type of action a UXAction is

    Possible Actions:
    Read - Present user with posts from a Post iterator/Selection executor
    Recall - Output text of a previously defined criteria or selection
    Error - Display error message
    Change Mode - Keep running as normal, enter the mode given in the action
    NOOP - Do nothing, continue as usual
    """
    READ = 0            # Data is a selection executor
    RECALL = 1          # Data is a list of strings
    ERROR = 2           # Data is an exception
    CHANGE_MODE = 3     # TODO
    NO_OP = 4           # Data is None
