from lark import Visitor

from derp.exceptions import SemanticException


class CheckSaveX(Visitor):
    def __init__(self, is_criteria, is_selection, is_selection_mode):
        self.__is_criteria = is_criteria
        self.__is_selection = is_selection
        self.__is_selection_mode = is_selection_mode

    def save_expression(self, node):
        assert len(node.children) == 1

        save_name = node.children[0]

        if self.__is_selection_mode():
            if self.__is_criteria(save_name):
                raise SemanticException(
                    "Criteria named '" + save_name + "' already exists")
        else:
            if self.__is_selection(save_name):
                raise SemanticException(
                    "Selection named '" + save_name + "' already exists")
