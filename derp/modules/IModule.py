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

    # Names must be unique when lower case
    def name(self):
        """
        :return: the name of the module
        """
        pass

    # Every rule or token must be prefixed with the module name to prevent rule name collisions
    # The only things this grammar may rely on are the following:
    # * The common lark ESCAPED_STRING is part of the grammar
    # * Whitespace will be ignored when parsing
    #
    # One rule must be [module name]_source, this is the rule that's matched
    #   to know when this module is to be used for a query
    # That rule must not begin with _ or ?. It may begin with !. It may be a token (all caps),
    #   or a rule (all lower-case)
    def source_grammar(self):
        """
        :return: the grammar for parsing sources interpreted by this module.
        """
        pass

    def post_definition(self):
        """
        :return: the PostDefinition which all posts returned from get_posts must match.
        """
        pass
