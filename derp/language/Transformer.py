"""
Transformer.py
Implementation for Transformer objects.

TODO: Semantic checks for
* Reading or Recalling a non-existing selection/criteria
* Reading a selection that requires unloaded modules
* Check that string data is non-empty
"""

from derp.language.ITransformer import ITransformer
from derp.exceptions.exceptions import SemanticException

from derp.language.qualifier_reductions.DateQualifierReducer import DateQualifierReducer
from derp.language.qualifier_reductions.SubstringQualifierReducer import SubstringQualifierReducer
from derp.language.qualifier_reductions.StringQualifierReducer import StringQualifierReducer
from derp.language.qualifier_reductions.BoolQualifierReducer import BoolQualifierReducer
from derp.language.qualifier_reductions.NumberQualifierReducer import NumberQualifierReducer
from derp.language.qualifier_reductions.AboutQualifierReducer import AboutQualifierReducer
from derp.language.qualifier_reductions.MatchingQualifierReducer import MatchingQualifierReducer

from lark import Transformer as LarkTransformer
from lark import Visitor as LarkVisitor
from lark import Tree as LarkTree, Token as LarkToken


class Transformer(ITransformer):
    """
    Defines the transform function which performs semantic analysis and macro expansion on an AST
    as provided by an IParser.
    """

    class StringQuoteRemover(LarkTransformer):
        """
        Find all string rules and remove the quotes around them, turning them into
        STRING tokens.
        """

        def string(self, args):
            unquoted_string = args[0][1:-1]

            if len(unquoted_string) == 0:
                raise SemanticException("Strings must not be empty")

            return LarkToken('STRING', unquoted_string)

    class ModuleSourceTransformer(LarkTransformer):
        def source_module(self, args):
            # Should only have 1 child, an ast for some module source grammar
            assert(len(args) == 1)

            # Child will be either a lark tree or token; no other options
            node_name = args[0].data if isinstance(
                args[0], LarkTree) else args[0].type

            # Parse the name of the module from the child's node type
            name_parts = node_name.split('_')

            # All sources should be '{modulename}_source'
            assert(len(name_parts) == 2)

            # Filter out non alpha-numeric characters from the lower case version of the module name
            module_name = "".join(
                x if x.isalnum() else '' for x in name_parts[0].lower())

            return LarkTree("source_module", [module_name, args[0]])

    def transform(self, ast):
        """
        Performs semantic analysis on the input tree and macro expansion.
        Returns the transformed AST if the input is semantically correct.
        May raise derp.exceptions.SemanticException.
        :param ast: a parse tree as created by an IParser
        :return: A transformed, semantically valid AST
        """

        qualifier_reduce = DateQualifierReducer() * SubstringQualifierReducer() * \
            StringQualifierReducer() * BoolQualifierReducer() * \
            NumberQualifierReducer() * AboutQualifierReducer()

        source_reduce = self.ModuleSourceTransformer()
        string_reduce = self.StringQuoteRemover()

        reducer = string_reduce * qualifier_reduce * \
            source_reduce * MatchingQualifierReducer()

        ast = reducer.transform(ast)

        return ast
