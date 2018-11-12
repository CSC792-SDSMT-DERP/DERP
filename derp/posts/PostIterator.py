"""
PostIterator.py
Implementation of PostIterator objects.
"""


class PostIterator:
    """
    Adapts a post generator to a class based iterator representation.
    """

    def __init__(self, post_generator):
        """
        Initialize the iterator with a Python generator which returns post objects.

        :param post_generator: Python generator which continually yields the next post
        returned from a query.
        """
        self._post_generator = post_generator

    def __iter__(self):
        return self._post_generator()
