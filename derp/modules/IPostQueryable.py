"""
IPostQueryable.py

Interface declaration of PostQueryable objects.
"""


class IPostQueryable:
    """
    Resolves post queries as needed for post selections.
    """

    def get_posts(self, source_ast, qualifier_tree):
        """
        Retrieves posts from a source specified in the source AST which match a
        given qualifier tree.

        :param source_ast: A AST representing the source clause of a selection.
        :param qualifier_tree: A tree representing a logical expression which the posts must match.
        :return: a PostIterator which iterates over the returned set of posts
        """
        pass

