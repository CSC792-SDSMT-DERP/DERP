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

        try:
            # Function to raise exception from within list comp
            def raise_ex(): raise GrammarDefinitionException(
                "grammar nonterminal or production is not of type string")

            # Convert dict to tuple(str, tuple(str, str, str...)), raising exception if typecheck fails
            self._tuples = tuple((k if isinstance(k, str) else raise_ex(), tuple(x if isinstance(x, str) else (x if isinstance(x, str) else raise_ex()) for x in v))
                                 for k, v in grammar_productions.items())

            self._startsym = start_symbol
            if start_symbol is not None and start_symbol not in grammar_productions:
                raise GrammarDefinitionException(
                    "grammar start symbol is not in productions list")

        except GrammarDefinitionException:
            raise

        except Exception:
            raise GrammarDefinitionException(
                "structure of grammar definition is invalid")

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
    for g in grammars:
        for k, v in g.productions():
            merged_grammar[k] = merged_grammar[k] + \
                v if k in merged_grammar else v

        # Build set of all non-none start symbols
        if g.start_symbol() is not None:
            start_symbols.update(g.start_symbol())

    # Assume no start symbol
    new_start = None

    # If all grammars have same start symbol, just use that
    if len(start_symbols) == 1:
        new_start = start_symbols.pop()

    # Otherwise, make a new start symbol S_n, and production S_n -> S1 | S2....
    else:
        i = 0
        while "S_" + str(i) in merged_grammar:
            i += 1

        new_start = "S_" + str(i)
        merged_grammar[new_start] = start_symbols

    return Grammar(merged_grammar, new_start)
