"""
SelectionExecutor.py

Class definition for the SelectionExecutor object.
"""


class SelectionExecutor:
    """
    Returns the results of a DERP selection.
    """

    def __init__(self, post_iterator):
        """
        Create a SelectionExecutor which reads its results from a given PostIterator
        :param post_iterator: a PostIterator
        """
        self.__post_iterator = post_iterator

    def results(self):
        """
        Retrieve the results from this selection executor
        :return: a post iterator containing the selection results
        """
        return self.__post_iterator
