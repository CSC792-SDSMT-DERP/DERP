"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules.ModuleController import ModuleController
from derp.session.selection_execution.AbstractSelectionExecutorFactory import AbstractSelectionExecutorFactory


class SelectionExecutorFactory(AbstractSelectionExecutorFactory):

    def __init__(self):
        self.__module_controller = None  # type: ModuleController

    def set_module_controller(self, module_controller):
        """
        Set the ModuleController to use for interfacing with DERP modules.
        :param module_controller:
        :return:
        """
        self.__module_controller = module_controller

    def build_selection_executor(self, selection_ast):
        """
        Handles creating a SelectionExecutor for any READ commands.
        """
        pass
