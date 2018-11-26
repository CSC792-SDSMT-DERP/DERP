"""
PostIteratorMuxer.py

Class definition for PostIteratorMuxer objects.
"""
import typing

class PostIteratorMuxer:
    """
    PostIteratorMuxers multiplex one or more source PostIterators in a round-robin manner.
    This is used to provide a single iterator to read from for the PostReader.
    """

    def __init__(self, sources):
        self.__sources = sources  # type: typing.List

    def __iter__(self):
        self.__curr_iter = 0
        return self

    def __next__(self):
        next_post = None
        while next_post is None:
            if len(self.__sources) == 0:
                raise StopIteration
            next_iter = self.__sources[self.__curr_iter]
            try:
                next_post = next(next_iter)
            except StopIteration:
                self.__sources.remove(next_iter)

        self.__curr_iter += 1
        self.__curr_iter = self.__curr_iter % len(self.__sources)
        return next_post
