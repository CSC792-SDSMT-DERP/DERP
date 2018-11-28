from .Grammar import Grammar
from .Parser import Parser
from .Transformer import Transformer
from .SemanticChecker import SemanticChecker


class __DerpGrammars:
    def __init__(self):
        from .GrammarDefinitions import MAIN_MODE_GRAMMAR, SELECTION_MODE_GRAMMAR, CRITERIA_MODE_GRAMMAR

        self.__main_grammar = MAIN_MODE_GRAMMAR
        self.__select_grammar = SELECTION_MODE_GRAMMAR
        self.__criteria_grammar = CRITERIA_MODE_GRAMMAR

    def main_grammar(self):
        return self.__main_grammar

    def criteria_grammar(self):
        return self.__criteria_grammar

    def selection_grammar(self):
        return self.__select_grammar


__grammars = __DerpGrammars()

def build_main_mode_parser():
    return Parser(__grammars.main_grammar())

def build_selection_and_criteria_parsers(active_modules):
    assert(len(active_modules) != 0)

    # TODO enforce that source grammars are valid
    field_grammars = [module.post_definition().field_grammar()
                        for module in active_modules]
    source_grammars = [(module.name(), module.source_grammar(),)
                        for module in active_modules]

    # Build a list of all the {modulename}_source rules
    # that exist
    source_productions = []
    for name, grammar in source_grammars:
        # Module grammars must not define a start symbol
        assert(grammar.start_symbol() is None)

        # Do all text matching with lower case
        name_source = name.lower() + "_source"
        grammar_source = None

        # Find the grammar rule that is {modulename}_source
        # It can be all caps (token) or all lower case (rule), and may begin with !
        for key, productions in grammar.productions():
            alnum_key = ''.join(
                x if x.isalnum() or x == '_' else '' for x in key.lower())

            if name_source == alnum_key:
                grammar_source = key

        assert(grammar_source is not None)
        source_productions.append(
            grammar_source + " -> source_module")

    assert(len(source_productions) > 0)

    # Make a grammar that is just the rule 'source -> [each module source name]'
    source_rule_grammar = Grammar(
        {'source': source_productions}
    )

    source_grammars = [module.source_grammar()
                        for module in active_modules]

    criteria_parser = Parser(
        __grammars.criteria_grammar(),
        *field_grammars,
        *source_grammars,
        source_rule_grammar
    )
    selection_parser = Parser(
        __grammars.selection_grammar(),
        *field_grammars,
        *source_grammars,
        source_rule_grammar
    )

    return (selection_parser, criteria_parser,)
