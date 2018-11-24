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

    def __init__(self, load_criteria, get_loaded_fields, is_criteria, is_selection, module_exists, module_loaded,
                 any_modules_loaded):
        """
        :param load_criteria: function to get parse trees for each line of a criteria. Should raise TextParseException, SemanticException, or FileIOException on failure
        :param get_loaded_fields: function to get fields provided by loaded modules on a per-module basis. Returns tuple(tuple(str))
        :param is_criteria: boolean function to check if a criteria exists
        :param is_selection: boolean function to check if a selection exists
        :param module_exists: boolean function to check if a module exists, loaded or unloaded
        :param module_loaded: boolean function to check if a module is loaded
        :param any_modules_loaded: boolean function to check if at least 1 module is loaded
        """
        self.__load_criteria = load_criteria
        self.__get_loaded_fields = get_loaded_fields
        self.__is_criteria = is_criteria
        self.__is_selection = is_selection
        self.__module_exists = module_exists
        self.__module_loaded = module_loaded
        self.__any_modules_loaded = any_modules_loaded

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
        def selector(self, args):
            return LarkTree("selector", *args)

        def source_or(self, args):
            assert(len(args) == 2)

            return args[0] + args[1]

        def source_selection(self, args):
            assert(len(args) == 1)

            return [LarkTree("source_selection", args)]

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

            return [LarkTree("source_module", [module_name, args[0]])]

    def transform(self, ast):
        """
        Performs semantic analysis on the input tree and macro expansion.
        Returns the transformed AST if the input is semantically correct.
        May raise derp.exceptions.SemanticException.

        Semantic Checks
        * Date provided which doesn't exist
        * Exact date check requested, but month and/or day not specified

        * Main Mode
            * Recall X or Clear X but X does not exist
            * Read X but selection X does not exist
            * Load X but X doesn't exist
            * Load X but X is loaded
            * Unload X but X not loaded
            * Going to creation or selection mode with no modules loaded
        * Selection/Criteria Mode
            * Matching X but criteria X does not exist
            * Matching X but no modules are loaded to provide the fields used in X
            * Save as X but X already exists as other type

        :param ast: a parse tree as created by an IParser
        :return: A transformed, semantically valid AST
        """

        # Reducers to take qualifier_x nodes and convert the children to arg lists
        qualifier_reduce = DateQualifierReducer() * SubstringQualifierReducer() * \
            StringQualifierReducer() * BoolQualifierReducer() * \
            NumberQualifierReducer() * AboutQualifierReducer()

        # Parse module names in source nodes
        # And convert string nodes to STRING tokens with no quotes around them
        source_reduce = self.ModuleSourceTransformer()
        string_reduce = self.StringQuoteRemover()

        # Chain reducers in order
        reducer = string_reduce * qualifier_reduce * \
                  source_reduce * \
                  MatchingQualifierReducer(self.__is_criteria, self.__load_criteria)

        # Reduce; may raise Semantic Exceptions
        ast = reducer.transform(ast)

        # Perform other semantic checks

        return ast
