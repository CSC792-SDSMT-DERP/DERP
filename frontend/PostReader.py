"""
PostReader.py

Class definition for the PostReader object.
"""
from .IPostReader import IPostReader


class PostReader(IPostReader):
    """
    The PostReader handles presenting selection results to the user.
    The Repl provides the PostReader with an IPostIterator which provides
    the list of results.
    """

    def __init__(self):
        return

    def read_from(self, executor):
        """
        Gives application control over to the post reader
        until such time as it sees fit to return from this
        call. The post reader should drop all references to
        the executor at such a time.
        :param executor: an IPostReader that provides the posts to read
        :return: None
        """
        for post in executor.results():
            print("Source: {0}".format(post.source().name()))
            for field_name in post.definition().field_definitions():
                print("{0}: {1}".format(field_name, post.field_data(field_name)))
            print("")
