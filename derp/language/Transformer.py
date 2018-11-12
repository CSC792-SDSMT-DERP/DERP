"""
Transformer.py
Implementation for Transformer objects.
"""

from derp.language.ITransformer import ITransformer


class Transformer(ITransformer):
    """
    Defines the transform function which performs semantic analysis and macro expansion on an AST
    as provided by an IParser.
    """

    def transform(self, ast):
        """
        Performs semantic analysis on the input tree and macro expansion.
        Returns the transformed AST if the input is semantically correct.
        May raise derp.exceptions.SemanticException.
        :param ast: a parse tree as created by an IParser
        :return: A transformed, semantically valid AST
        """
        # TODO
        return ast
