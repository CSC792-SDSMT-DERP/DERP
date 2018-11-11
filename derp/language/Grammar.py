from derp.exceptions.exceptions import *


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

        # Function to raise exception from within list comp
        def raise_ex(): raise GrammarDefinitionException

        # Convert dict to tuple(str, tuple(str, str, str...)), raising exception if typecheck fails
        self._tuples = tuple((k if isinstance(k, str) else raise_ex(), tuple(x if isinstance(x, str) else (x if isinstance(x, str) else raise_ex()) for x in v))
                             for k, v in grammardef.items())

    def productions(self):
        """
        Returns the loaded grammar in the form of a tuple, where each element is a tuple
        with two items. The first is the first is the nonterminal produced, and the second is a tuple
        of strings containing productions for the nonterminal
        """
        return tuple()

    def start_symbol(self):
        """
        Gets the start symbol for the grammar.
        The result with either be one of the nonterminals in the grammar or None
        """
        return None


def merge_grammars(*grammars):
    """
    Merges multiple grammars to produce a new grammar

    raises GrammarMergeException
    """
    pass
