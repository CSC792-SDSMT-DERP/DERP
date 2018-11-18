"""
IPostIterator.py

Interface definition for PostIterator objects.
"""


class IPostIterator:
    """
    PostIterators provide the means to read posts one at a time using python's iterator syntax.
    """

    def __iter__(self):
        pass
