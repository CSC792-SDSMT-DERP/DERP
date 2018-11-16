"""
IPost.py
Interface declaration for Post objects.
"""


class IPost:
    """
    Encapsulates the information contained within postings returned by IPostQueryables.
    Each IPost implementor must specify a PostDefinition which outlines the type
    of data contained within the post.
    """

    def definition(self):
        """
        Retrieves the PostDefinition for a given post
        :return: a PostDefinition object describing the fields contained in this post.
        """
        pass

    def source(self):
        """
        Returns the module object which created a given post
        :return: the module object which created this post
        """

    def field_data(self, field_name):
        """
        Retrieves the data for a given field.
        It is highly suggested that implementors memoize this function.
        :param field_name: The name of the field to retrieve data for.
        :return: Field data matching the FieldType declared in the PostDefinition
        """
        pass

    def about(self, string):
        """
        Decides whether the field data contained in the post matches a given search string.
        :param string: the search string to consider
        :return: True if the post matches, and False if it does not.
        """
        pass
