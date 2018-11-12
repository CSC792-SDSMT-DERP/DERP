"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules.ModuleController import ModuleController
from derp.session.selection_execution.AbstractSelectionExecutorFactory import AbstractSelectionExecutorFactory


class SelectionExecutorFactory(AbstractSelectionExecutorFactory):

    def __init__(self, module_controller):
        self.__module_controller = module_controller  # type: ModuleController

    def build_selection_executor(self, selection_ast):
        """
        Handles creating a SelectionExecutor for any READ commands.
        """
        pass
