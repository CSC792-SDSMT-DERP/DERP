"""
Evaluator.py

Class definition for the Evaluator object
"""
from derp.session.IEvaluator import IEvaluator
from derp.session.SessionAction import *

from lark import Visitor, v_args


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

        result_action = None

        class EvalVisitor(Visitor):
            def stop_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 0)

                result_action = SessionAction(
                    SessionActionType.CHANGE_MODE, SessionActionModeType.EXIT)

            def load_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.LOAD_MODULE, tree.children[0])

            def unload_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.UNLOAD_MODULE, tree.children[0])

            def clear_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.CLEAR_BUFFER, tree.children[0])

            def save_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.SAVE_BUFFER, tree.children[0])

            def add_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.APPEND_TO_BUFFER, None)

            def remove_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                result_action = SessionAction(
                    SessionActionType.APPEND_TO_BUFFER, None)

            def read_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1 or len(tree.children) == 0)

                target = None if len(tree.children) == 0 else tree.children[0]
                result_action = SessionAction(
                    SessionActionType.QUERY, target)

            def recall_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1 or len(tree.children) == 0)

                target = None if len(tree.children) == 0 else tree.children[0]
                result_action = SessionAction(
                    SessionActionType.RECALL, target)

            def create_expression(self, tree):
                nonlocal result_action
                assert(len(tree.children) == 1)

                create_type = tree.children[0].type

                new_mode = None
                if create_type == "CRITERIA":
                    new_mode = SessionActionModeType.CRITERIA
                elif create_type == "SELECTION":
                    new_mode = SessionActionModeType.SELECTION
                else:
                    assert(False)

                result_action = SessionAction(
                    SessionActionType.CHANGE_MODE, new_mode)

        EvalVisitor().visit(semantic_tree)

        assert(result_action is not None)

        return result_action
