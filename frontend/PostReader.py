"""
PostReader.py

Class definition for the PostReader object.
"""
from frontend.IPostReader import IPostReader


class PostReader(IPostReader):
    """
    The PostReader handles presenting selection results to the user.
    The Repl provides the PostReader with an IPostIterator which provides
    the list of results.
    """

    def __init__(self):
        self.__repl = None

    def set_repl(self, repl):
        self.__repl = repl
