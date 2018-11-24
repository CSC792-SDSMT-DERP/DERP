"""
AbstractSelectionExecutorFactory.py

Interface definition for SelectionExecutorFactory objects.
"""


class AbstractSelectionExecutorFactory:
    """
    SelectionExecutorFactories must be able to build SelectionExecutors from an AST.
    """

    def build_selection_executor(self, selection_ast_list):
        """
        Handles creating a SelectionExecutor for any READ commands.
        :param selection_ast_list: A list of line by line ASTs
        """
        pass
