"""
ISessionStateController.py

Interface definition for SessionStateController objects.
"""


class ISessionStateController:
    """
    SessionStateControllers are expected to be capable of saving and loading selections and criteria, and returning the
    internal Buffer object that stores the strings representing them.
    """

    def save_criteria(self, name):
        """
        Saves the the list of statements in the buffer as a new criterion.
        :raises IOException: raised if a save fails
        :param name: name to save the criteria under
        :return: None
        """
        pass

    def load_criteria(self, name):
        """
        Loads the named criterion into the buffer.
        :raises IOException: raised if a load fails
        :param name: name of the criteria to load
        :return: list of strings representing the criteria
        """
        pass

    def save_selection(self, name):
        """
        Saves the list of statements in the buffer as a new selection.
        :raises IOException: raised if a save fails
        :param name: name to save the selection under
        :return: None
        """
        pass

    def LoadSelection(self, name):
        """
        Loads the named selection into the buffer.
        :raises IOException: raised if a load fails
        :param name: name of the selection to load
        :return: list of strings representing the criteria
        """
        pass

    def get_buffer(self):
        """
        Returns the current buffer.
        :return:
        """
        pass

