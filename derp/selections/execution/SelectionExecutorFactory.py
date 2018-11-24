"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules import ModuleController
from derp.selections import Selection, AddSelectionExpression, RemoveSelectionExpression
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
        for expression in selection.expressions:
            if isinstance(expression, AddSelectionExpression):
                print("Query source {0} for posts matching {1}".format(", ".join(expression.source_asts()), expression.qualifier_tree()))
            elif isinstance(expression, RemoveSelectionExpression):
                print("Remove posts matching {0}".format(expression.qualifier_tree()))
        
        # TODO Sort statements into bins based on which sources they affect. Then merge the q_trees and dispatch to the module controller.
        pass
