
from derp.exceptions import TextParseException
from derp.language.IParser import IParser


class Parser (IParser):
    """
    Implementation of the IParser interface, utilizing the Python Lark parser
    """

    def set_grammar(self, *grammars):
        """
        Gives the parser multiple grammars to combine into a new
        grammar, which will be loaded as the active grammar for parsing

        raises GrammarMergeException
        raises GrammarDefinitionException
        """
        pass

    def parse(self, text):
        """
        Parses a line of text using the grammar created in the most recent call to setSyntax,
        returns the AST produced by the Lark Parser

        raises TextParseException
        """
        raise TextParseException("parsing is unimplemented")
