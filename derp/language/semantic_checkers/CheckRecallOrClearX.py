from lark import Visitor

from derp.exceptions import *


class CheckRecallOrClearX(Visitor):
    def __init__(self, is_criteria, is_selection):
        self.__is_criteria = is_criteria
        self.__is_selection = is_selection

    def _check_node(self, node):
        assert(len(node.children) == 0 or len(node.children) == 1)

        if len(node.children) == 1:
            selection_or_criteria_name = node.children[0]

            if not self.__is_criteria(selection_or_criteria_name) and not self.__is_selection(selection_or_criteria_name):
                raise MissingIdSException(
                    "Selection or Criteria '" + selection_or_criteria_name + "' does not exist")

    def recall_expression(self, node):
        self._check_node(node)

    def clear_expression(self, node):
        self._check_node(node)
