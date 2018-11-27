"""
IEvaluator.py

Interface definition for Evaluator objects.
"""


class IEvaluator:
    """
    Evaluators must be able to take in Abstract Syntax Trees containing semantic
    """

    def evaluate(self, input_line, semantic_tree):
        """
        Determines what action to take given the provided semantically analyzed AST.
        These actions may include performing a query or passing a UXAction to the REPL.
        :param input_line: the line that was parsed into the semantic tree
        :param semantic_tree: semantic_tree to evaluate
        :return: SessionAction representing commands for the SessionController to execute
        """
        pass

