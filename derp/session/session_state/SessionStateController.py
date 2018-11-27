"""
SessionStateController.py

Class definition for the SessionStateController object.
"""
import os

from .FileManager import FileManager
from .Buffer import SelectionBuffer, CriterionBuffer
from .IBuffer import IBuffer
from .ISessionStateController import ISessionStateController

from derp.exceptions import FileIOException


class SessionStateController(ISessionStateController):
    """
    The SessionStateController manages saving and loading operations via the FileManager.
    The SessionStateController is also responsible for managing the "savable" buffer of statements.
    """

    def __init__(self, file_manager):
        self.__buffer = None
        self.__file_manager = file_manager  # type: FileManager

    def save_criteria(self, name):
        """
        Saves the the list of statements in the buffer as a new criterion.
        :raises FileIOException: raised if a save fails
        :param name: name to save the criteria under
        :return: None
        """
        try:
            self.__file_manager.write_file(os.path.join(
                "criteria", name), self.__buffer.get_commands())
        except FileIOException as e:
            raise e

    def load_criteria(self, name):
        """
        Loads the named criterion and returns it as a list of lines
        :raises FileIOException: raised if a load fails
        :param name: name of the criteria to load
        :return: list of str
        """
        try:
            lines = self.__file_manager.read_file(
                os.path.join("criteria", name))

            return lines
        except FileIOException as e:
            raise e

    def delete_criteria(self, name):
        """
        Deletes the criteria with the given name
        :param name: name of the criteria to delete
        :raises FileIOException: raised if deletion fails
        """
        try:
            self.__file_manager.delete_file(os.path.join("criteria", name))
        except FileIOException as e:
            raise e

    def save_selection(self, name):
        """
        Saves the list of statements in the buffer as a new selection.
        :raises FileIOException: raised if a save fails
        :param name: name to save the selection under
        :return: None
        """
        try:
            self.__file_manager.write_file(os.path.join(
                "selections", name), self.__buffer.get_commands())
        except FileIOException as e:
            raise e

    def load_selection(self, name):
        """
        Loads the named selection and returns the file text as a list of lines
        :raises FileIOException: raised if a load fails
        :param name: name of the selection to load
        :return: list of str
        """
        try:
            lines = self.__file_manager.read_file(
                os.path.join("selections", name))

            return lines
        except FileIOException as e:
            raise e

    def delete_selection(self, name):
        """
        Deletes the selection with the given name
        :param name: name of the selection to delete
        :raises FileIOException: raised if deletion fails
        """
        try:
            self.__file_manager.delete_file(os.path.join("selections", name))
        except FileIOException as e:
            raise e

    def selection_exists(self, name):
        """
        Checks if a selection exists with the given name. This does not
        guarantee the selection will not fail to load
        :param name: name of the selection to check for
        """
        try:
            return self.__file_manager.file_exists(os.path.join("selections", name))
        except FileIOException:
            return False

    def criteria_exists(self, name):
        """
        Checks if a criteria exists with the given name. This does not
        guarantee the criteria will not fail to load
        :param name: name of the criteria to check for
        """
        try:
            return self.__file_manager.file_exists(os.path.join("criteria", name))
        except FileIOException:
            return False

    def set_buffer_to_new_criteria_buffer(self):
        """
        Ensures the result from get_buffer is an empty buffer for building criteria
        """
        self.__buffer = CriterionBuffer()

    def set_buffer_to_new_selection_buffer(self):
        """
        Ensures the result from get_buffer is an empty buffer for building selections
        """
        self.__buffer = SelectionBuffer()

    def disable_buffer(self):
        """
        Ensures the result from get_buffer is None (used for main mode)
        """
        self.__buffer = None

    def get_buffer(self):
        """
        Returns the current buffer.
        :rtype: IBuffer
        :return: the current buffer
        """
        return self.__buffer
