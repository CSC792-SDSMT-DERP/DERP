"""
IModule.py

Interface definition for DERP modules.
"""

from derp.modules.IPostQueryable import IPostQueryable


class IModule(IPostQueryable):
    """
    Interface for query resolving DERP modules. Each module must supply a module name, grammar for
    parsing source clauses, a query resolver as per IPostQueryable, and a PostDefinition which all returned
    posts much match.
    """

    def name(self):
        """
        :return: the name of the module
        """
        pass

    def source_grammar(self):
        """
        TODO
        :return: the grammar for parsing sources interpreted by this module.
        """
        pass

    def post_definition(self):
        """
        :return: the PostDefinition which all posts returned from get_posts must match.
        """
        pass

