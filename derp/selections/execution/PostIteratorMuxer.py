"""
PostIteratorMuxer.py

Class definition for PostIteratorMuxer objects.
"""


class PostIteratorMuxer:
    """
    PostIteratorMuxers multiplex one or more source PostIterators in a round-robin manner.
    This is used to provide a single iterator to read from for the PostReader.
    """

    def __init__(self, sources):
        self.__sources = sources

    def __iter__(self):
        self.__curr_iter = 0
        return self

    def __next__(self):
        next_iter = self.__sources[self.__curr_iter]
        self.__curr_iter += 1
        self.__curr_iter = self.__curr_iter % len(self.__sources)
        return next(next_iter)
