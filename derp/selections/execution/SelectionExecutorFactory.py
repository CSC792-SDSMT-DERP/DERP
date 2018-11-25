"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules import ModuleController
from derp.selections import Selection, AddSelectionExpression, RemoveSelectionExpression
from .PostIteratorFilter import *
from .PostIteratorMuxer import *
from .SelectionExecutor import *
from .AbstractSelectionExecutorFactory import AbstractSelectionExecutorFactory
import os
import os.path


class SelectionExecutorFactory(AbstractSelectionExecutorFactory):

    def __init__(self, module_controller):
        self.__module_controller = module_controller  # type: ModuleController

    def build_selection_executor(self, selection_ast_list):
        """
        Handles creating a SelectionExecutor for any READ commands.
        :param selection_ast_list: A list of line by line ASTs
        """
        selection = Selection(selection_ast_list)
        expressions_per_source = {}

        for expression in selection.expressions:
            if isinstance(expression, AddSelectionExpression):
                print("Query source {0} for posts matching {1}".format(
                    ", ".join([str(x) for x in expression.source_asts()]), expression.qualifier_tree()))

                for ast in expression.source_asts():
                    if ast.data == "source_module":
                        target_module = ast.children[0]
                        if ast in expressions_per_source:
                            expressions_per_source[ast].append(expression)
                        else:
                            expressions_per_source[ast] = [expression]

                    # TODO Maybe here? : Handle source_selection

            elif isinstance(expression, RemoveSelectionExpression):
                print("Remove posts matching {0}".format(
                    expression.qualifier_tree()))

                for ast, exprs in expressions_per_source.items():
                    exprs.append(expression)

        # TODO : Combine expressions into a single predicate tree
        for source_ast, exprs in expressions_per_source.items():
            if ast.data == "source_module":

                # TODO : Pass actual qualifier tree
                #        Collect post iterators wrapped in post iterator filters for the appropriate qualifier trees
                post_iterator = self.__module_controller.get_posts(
                    source_ast, None)

        # TODO : Create a post iterator muxer from the post iterator filter wrappers
        #        Return that muxer, wrapped as a SelectionExecutor
        from derp.posts import PostIterator
        return SelectionExecutor(PostIterator(None))
