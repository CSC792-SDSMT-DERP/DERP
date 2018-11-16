"""
PostIteratorMuxer.py

Class definition for PostIteratorMuxer objects.
"""


class PostIteratorMuxer:
    """
    PostIteratorMuxers multiplex one or more source PostIterators in a round-robin manner.
    This is used to provide a single iterator to read from for the PostReader.
    """

    def __init__(self, sources=None):
        self.__sources = sources if sources else []

    def __iter__(self):
        self.__curr_iter = 0

    def __next__(self):
        value = self.__sources[self.__curr_iter]
        self.__curr_iter += 1
        self.__curr_iter = self.__curr_iter == len(self.__sources) if 0 else self.__curr_iter

    def add_source_iter(self, source_iter):
        self.__sources.append(source_iter)
