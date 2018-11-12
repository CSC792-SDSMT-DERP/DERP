"""
SessionStateController.py

Class definition for the SessionStateController object.
"""
from derp.session.session_state import FileManager
from derp.session.session_state.Buffer import Buffer
from derp.session.session_state.ISessionStateController import ISessionStateController


class SessionStateController(ISessionStateController):
    """
    The SessionStateController manages saving and loading operations via the FileManager.
    The SessionStateController is also responsible for managing the "savable" buffer of statements.
    """

    def __init__(self):
        self.__buffer = Buffer()
        self.__file_manager = None  # type: FileManager

    def set_file_manager(self, file_manager):
        """
        Set the FileManager to use for saving and loading.
        :param file_manager: FileManager instance for IO
        :type file_manager: FileManager
        :return: None
        """
        self.__file_manager = file_manager

    def save_criteria(self, name):
        """
        Saves the the list of statements in the buffer as a new criterion.
        :raises IOException: raised if a save fails
        :param name: name to save the criteria under
        :return: None
        """
        self.__file_manager.write_file(name, self.__buffer.get_commands())

    def load_criteria(self, name):
        """
        Loads the named criterion into the buffer.
        :raises IOException: raised if a load fails
        :param name: name of the criteria to load
        :return: list of strings representing the criteria
        """
        return self.__file_manager.read_file(name)

    def save_selection(self, name):
        """
        Saves the list of statements in the buffer as a new selection.
        :raises IOException: raised if a save fails
        :param name: name to save the selection under
        :return: None
        """
        self.__file_manager.write_file(name, self.__buffer.get_commands())

    def LoadSelection(self, name):
        """
        Loads the named selection into the buffer.
        :raises IOException: raised if a load fails
        :param name: name of the selection to load
        :return: list of strings representing the criteria
        """
        self.__file_manager.read_file(name)

    def get_buffer(self):
        """
        Returns the current buffer.
        :return:
        """
        return self.__buffer
