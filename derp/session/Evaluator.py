"""
Evaluator.py

Class definition for the Evaluator object
"""
from derp.session.IEvaluator import IEvaluator


class Evaluator(IEvaluator):
    """
    The Evaluator determines what SessionAction the SessionController should perform for a given input.
    """

    def evaluate(self, semantic_tree):
        """
        Determines what action to take given the provided semantically analyzed AST.
        These actions may include performing a query or passing a UXAction to the REPL.
        :param semantic_tree: semantic_tree to evaluate
        :return: SessionAction representing commands for the SessionController to execute
        """
        # TODO: evaluate a given semantic tree
        pass