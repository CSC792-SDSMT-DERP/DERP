"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules import ModuleController
from .AbstractSelectionExecutorFactory import AbstractSelectionExecutorFactory


class SelectionExecutorFactory(AbstractSelectionExecutorFactory):

    def __init__(self, module_controller):
        self.__module_controller = module_controller  # type: ModuleController

    def build_selection_executor(self, selection_ast_list):
        """
        Handles creating a SelectionExecutor for any READ commands.
        :param selection_ast_list: A list of line by line ASTs
        """

        for ast in selection_ast_list:
            # TODO
            """
            if is_add(ast):
                convert ast to multiple (source, pred tree) pairs and dispatch to module controller
            else if is_remove(ast):
                wire in remove iterator
            """
        pass
