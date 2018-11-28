"""
PostIteratorFilter.py

Class definition for PostIteratorFilter objects.
"""
import typing

class PostIteratorFilter:
    """
    PostIteratorFilter takes in an iterator and filters out posts which do not match a given qualifier tree.
    It will continue to drain the source iterator until it finds a post which matches the qualifier tree.
    """

    MAX_CONSECUTIVE_FAILS = 25

    def __init__(self, source_post_iter, qualifier_tree):
        self.__source_post_iter = source_post_iter
        self.__q_tree = qualifier_tree
        self.__fails = 0

    def __iter__(self):
        return self

    def __next__(self):
        next_post = next(self.__source_post_iter)
        if self.__q_tree is not None:
            while not self.__q_tree.evaluate(next_post):
                self.__fails+=1

                # Exit after 25 consecutive fails
                if self.__fails == self.MAX_CONSECUTIVE_FAILS:
                    raise StopIteration
                next_post = next(self.__source_post_iter)

        self.__fails = 0
        return next_post
