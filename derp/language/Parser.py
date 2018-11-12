
from derp.language.IParser import IParser
from derp.language.Grammar import *
from derp.exceptions.exceptions import *

from lark import Lark


class Parser (IParser):
    """
    Implementation of the IParser interface, utilizing the Python Lark parser
    """

    def __init__(self):
        self._parser = None

    def set_grammar(self, *grammars):
        """
        Gives the parser multiple grammars to combine into a new
        grammar, which will be loaded as the active grammar for parsing

        raises GrammarMergeException
        raises GrammarDefinitionException
        """

        new_grammar = merge_grammars(*grammars)
        self._parser = build_lark_parser(new_grammar)

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
        except Exception as ex:
            raise TextParseException(
                "error parsing text '" + text + "' (" + ex.args[0] + ")") from ex

        # Can this even happen?
        if ast is None:
            raise TextParseException("Lark parser returned None ast??")

        return ast
