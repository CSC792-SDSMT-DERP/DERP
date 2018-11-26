from lark import Visitor

from derp.exceptions import SemanticException


class CheckReadX(Visitor):
    def __init__(self, is_selection):
        self.__is_selection = is_selection

    def read_expression(self, node):
        assert (len(node.children) == 0 or len(node.children) == 1)

        if len(node.children) == 1:
            selection_name = node.children[0]

            if not self.__is_selection(selection_name):
                raise SemanticException(
                    "Selection '" + selection_name + "' does not exist")
