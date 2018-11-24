"""
Transformer.py
Implementation for Transformer objects.

TODO: Semantic checks for
* Reading or Recalling a non-existing selection/criteria
* Reading a selection that requires unloaded modules
* Check that string data is non-empty
"""

from .ITransformer import ITransformer
from .qualifier_reductions import *
from derp.exceptions import SemanticException

from lark import Transformer as LarkTransformer
from lark import Tree as LarkTree, Token as LarkToken


class Transformer(ITransformer):

    def __init__(self, load_asts, is_criteria, is_selection):
        """
        :param load_asts: function to get parse trees for each line of a criteria or selection. Should raise TextParseException, SemanticException, or FileIOException on failure
        :param is_criteria: boolean function to check if a criteria exists
        :param is_selection: boolean function to check if a selection exists
        """
        self.__load_asts = load_asts
        self.__is_criteria = is_criteria
        self.__is_selection = is_selection

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
        def __init__(self, load_asts, selection_exists):
            self.__load_asts = load_asts
            self.__selection_exists = selection_exists

        def source_or(self, args):
            assert(len(args) == 2)

            new_children = []

            for child in args:
                if child.data == "source_or":
                    new_children = new_children + child.children
                else:
                    new_children.append(child)

            return LarkTree("source_or", new_children)

        def source_selection(self, args):
            assert(len(args) == 1)

            selection_name = args[0]

            if not self.__selection_exists(selection_name):
                raise SemanticException(
                    "Selection '" + selection_name + "' does not exist")

            asts = get_subtitute_ast_list(self.__load_asts, selection_name)

            return LarkTree("source_selection", [asts, selection_name])

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
        Reduces the Lark AST, producing the defined DERP interpreter ast
        Performs some DERP semantic checks. The remaining semantic checks are performed
        by the SemanticChecker type
        Returns the transformed AST
        May raise derp.exceptions.SemanticException.

        Semantic Checks
           * Date used in date check is not a valid date
           * Date used in 'on date' check does not specify day and month
           * matching criteria check or add from selection results in recursive query
           * Matching X but criteria X does not exist
           * Matching X but no modules are loaded to provide the fields used in X
           * Add from X but selection X does not exist

        :param ast: a parse tree as created by an IParser
        :return: A transformed, semantically valid AST
        """

        # Reducers to take qualifier_x nodes and convert the children to arg lists
        qualifier_reduce = DateQualifierReducer() * SubstringQualifierReducer() * \
            StringQualifierReducer() * BoolQualifierReducer() * \
            NumberQualifierReducer() * AboutQualifierReducer()

        # Parse module names in source nodes
        # And convert string nodes to STRING tokens with no quotes around them
        source_reduce = self.ModuleSourceTransformer(
            self.__load_asts, self.__is_selection)
        string_reduce = self.StringQuoteRemover()

        # Chain reducers in order
        reducer = string_reduce * qualifier_reduce * \
            source_reduce * \
            MatchingQualifierReducer(self.__is_criteria, self.__load_asts)

        # Reduce; may raise Semantic Exceptions
        ast = reducer.transform(ast)


        return ast
