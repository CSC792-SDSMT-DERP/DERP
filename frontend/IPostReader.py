"""
IPostReader.py

Interface definition for PostReader objects.
"""

class IPostReader:
    """
    IPostReaders provide a method to read from a PostIterator.
    """

    def read_from(self, executor):
        """
        Gives application control over to the post reader
        until such time as it sees fit to return from this
        call. The post reader should drop all references to
        the executor at such a time.
        :param executor: an IPostReader that provides the posts to read
        :return: None
        """
        pass