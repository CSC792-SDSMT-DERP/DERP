
from .IParser import IParser
from .Grammar import *

from derp.exceptions import *

from lark import Lark
from lark.exceptions import UnexpectedInput, ParseError


class Parser (IParser):
    """
    Implementation of the IParser interface, utilizing the Python Lark parser
    """

    def __init__(self, *grammars):
        """
        Gives the parser multiple grammars to combine into a new
        grammar, which will be loaded as the active grammar for parsing

        raises GrammarMergeException
        raises GrammarDefinitionException
        """
        if len(grammars):
            new_grammar = merge_grammars(*grammars)
            self._parser = build_lark_parser(new_grammar)
        else:
            self._parser = None

    def parse(self, text):
        """
        Parses a line of text using the grammar created in the most recent call to setSyntax,
        returns the AST produced by the Lark Parser

        raises TextParseException
        """

        if self._parser is None:
            raise TextParseException("no grammar loaded")

        ast = None
        try:
            ast = self._parser.parse(text)
        except UnexpectedInput as ex:
            raise TextParseException(
                '%s at line %s, column %s.\n\n%s' % ("Parse Error", ex.line, ex.column, ex.get_context(text))) from ex
        except ParseError as ex:
            raise TextParseException(str(ex)) from ex

        # Can this even happen?
        if ast is None:
            raise TextParseException("Lark parser returned None ast??")

        return ast
