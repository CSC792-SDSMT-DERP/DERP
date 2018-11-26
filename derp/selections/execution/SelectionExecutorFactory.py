"""
SelectionExecutorFactory.py

Class definition for the SelectionExecutorFactory object.
"""
from derp.modules import ModuleController
from derp.selections import Selection
from .PostIteratorMuxer import *
from .SelectionExecutor import *
from .AbstractSelectionExecutorFactory import AbstractSelectionExecutorFactory

class SelectionExecutorFactory(AbstractSelectionExecutorFactory):

    def __init__(self, module_controller):
        self.__module_controller = module_controller  # type: ModuleController

    def build_selection_executor(self, selection_ast_list):
        """
        Handles creating a SelectionExecutor for any READ commands.
        :param selection_ast_list: A list of line by line selection ASTs
        :return: a selection executor which retrieves posts for the selection
        """
        selection = Selection(selection_ast_list)
        source_ast_qualifier_tree_map = selection.source_ast_qualifier_tree_map()

        post_iterators = []
        for source_ast, qualifier_tree in source_ast_qualifier_tree_map.items():
            print("Retrieving posts from {0} matching {1}".format(source_ast, qualifier_tree))
            assert source_ast.data == "source_module"
            post_iterators.append(self.__module_controller.get_posts(source_ast, qualifier_tree)
                                  )
        return SelectionExecutor(PostIteratorMuxer(post_iterators))
