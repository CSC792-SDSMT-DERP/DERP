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

    def __init__(self, source_post_iter, qualifier_tree):
        self.__source_post_iter = source_post_iter
        self.__q_tree = qualifier_tree

    def __iter__(self):
        return self

    def __next__(self):
        next_post = next(self.__source_post_iter)
        if self.__q_tree is not None:
            while not self.__q_tree.evaluate(next_post):
                next_post = next(self.__source_post_iter)

        return next_post
