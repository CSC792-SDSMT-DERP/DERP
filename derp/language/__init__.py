from .Grammar import Grammar
from .Parser import Parser
from .Transformer import Transformer


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


grammars = __DerpGrammars()
