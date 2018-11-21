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
        :raises FileIOException: raised if a save fails
        :param name: name to save the criteria under
        :return: None
        """
        pass

    def load_criteria(self, name):
        """
        Loads the named criterion and returns it as a list of strings
        :raises FileIOException: raised if a load fails
        :param name: name of the criteria to load
        :return: list of strings representing the criteria
        """
        pass

    def delete_criteria(self, name):
        """
        Deletes the criteria with the given name
        :param name: name of the criteria to delete
        :raises FileIOException: raised if deletion fails
        """
        pass

    def save_selection(self, name):
        """
        Saves the list of statements in the buffer as a new selection.
        :raises FileIOException: raised if a save fails
        :param name: name to save the selection under
        :return: None
        """
        pass

    def load_selection(self, name):
        """
        Loads the named selection and returns it as a list of strings
        :raises FileIOException: raised if a load fails
        :param name: name of the selection to load
        :return: list of strings representing the criteria
        """
        pass

    def delete_selection(self, name):
        """
        Deletes the selection with the given name
        :param name: name of the selection to delete
        :raises FileIOException: raised if deletion fails
        """
        pass

    def selection_exists(self, name):
        """
        Checks if a selection exists with the given name. This does not
        guarantee the selection will not fail to load
        :param name: name of the selection to check for
        """
        pass

    def criteria_exists(self, name):
        """
        Checks if a criteria exists with the given name. This does not
        guarantee the criteria will not fail to load
        :param name: name of the criteria to check for
        """
        pass

    def get_buffer(self):
        """
        Returns the current buffer.
        :return: returns the Buffer object that the SessionStateController is using
        """
        pass
