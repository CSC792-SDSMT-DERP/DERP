from derp.exceptions.exceptions import *

from lark import Lark


class Grammar (dict):
    """
    Type checking container to hold information about the grammar to be
    used to construct a lark parser
    """

    def __init__(self, grammar_productions, start_symbol=None):
        """
        Initializes a Grammar. Input must have the following behavior:
        * Have a .items() method that returns an x,y iterator, as a dict
        * Each x from the above iterator must be a string
        * Each y must be either a string, or a 1-dimensional iterable of strings

        Given such a string x and string or set of strings y, x represents a Grammar nonterminal,
        and each y string represents a production for that nonterminal

        If start_symbol is not None, then it must be one of the keys x
        If start_symbol is None, then the Grammar must be merged with another grammar
        containing a start symbol before it is valid

        raises GrammarDefinitionException if the input does not follow this behavior
        """

        try:
            # Convert dict to tuple(str, tuple(str, str, str...)), raising exception if typecheck fails
            self._tuples = tuple((k, (v,) if isinstance(v, str) else tuple(x for x in v))
                                 for k, v in grammar_productions.items())

        except Exception as ex:
            raise GrammarDefinitionException(
                "structure of grammar definition is invalid") from ex

        if start_symbol is not None and start_symbol not in grammar_productions:
            raise GrammarDefinitionException(
                "grammar start symbol is not in productions list")

        self._startsym = start_symbol

    def productions(self):
        """
        Returns the loaded grammar in the form of a tuple, where each element is a tuple
        with two items. The first is the first is the nonterminal produced, and the second is a tuple
        of strings containing productions for the nonterminal
        """
        return self._tuples

    def start_symbol(self):
        """
        Gets the start symbol for the grammar.
        The result with either be one of the nonterminals in the grammar or None
        """
        return self._startsym


def merge_grammars(*grammars):
    """
    Merges multiple grammars to produce a new grammar

    If the grammars have distinct non-empty start symbols S1, S2, S3... then a new start symbol
    S_n will be added to the Grammar along with the production S_n -> S1 | S2 | S3... where n is chosen
    to avoid conflicts

    raises GrammarMergeException
    """

    merged_grammar = {}
    start_symbols = set()

    # Merge all productions together
    try:
        for g in grammars:
            for k, v in g.productions():
                merged_grammar[k] = merged_grammar[k] + \
                    v if k in merged_grammar else v

            # Build set of all non-none start symbols
            if g.start_symbol() is not None:
                start_symbols.update([g.start_symbol()])

    except Exception as ex:
        raise GrammarMergeException("unable to merge grammars (" + ex.args[0] + ")") from ex

    # Assume no start symbol
    new_start = None

    # If all grammars have same start symbol, just use that
    if len(start_symbols) == 1:
        new_start = start_symbols.pop()

    # Otherwise, make a new start symbol S_n, and production S_n -> S1 | S2....
    elif len(start_symbols) > 1:
        i = 0
        while "s_" + str(i) in merged_grammar:
            i += 1

        new_start = "s_" + str(i)
        merged_grammar[new_start] = start_symbols

    return Grammar(merged_grammar, new_start)


def convert_productions_to_lark_grammar(productions):

    # Start with common grammar rules - escaped strings, signed numbers, and whitespace ignoring
    string_grammar = r"""
%import common.ESCAPED_STRING -> STRING
%import common.WS
%ignore WS
"""

    # Add a line to the grammar for each item in the productions list
    # The line will be of the form 'nonterminal : (production) | (production) | (production)...'
    for nonterminal_rule in productions:
        string_production = nonterminal_rule[0] + \
            " : " + nonterminal_rule[1][0] + "\n"

        for production in nonterminal_rule[1][1:]:
            string_production += " | " + production + "\n"

        string_grammar += "\n" + string_production

    return string_grammar


def build_lark_parser(grammar):
    """
    Converts a grammar object into a Lark parser

    raises GrammarDefinitionException
    """

    if grammar.start_symbol() is None:
        raise GrammarDefinitionException(
            "no start symbol defined in grammar")

    string_grammar = convert_productions_to_lark_grammar(grammar.productions())

    try:
        return Lark(string_grammar, start=grammar.start_symbol())
    except Exception as ex:
        raise GrammarDefinitionException(
            "unable to produce Lark parser (" + ex.args[0] + ")") from ex
