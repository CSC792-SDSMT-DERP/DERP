from lark import Visitor

from derp.exceptions import *


class CheckSaveNonEmpty(Visitor):
    def __init__(self, buffer_size, is_selection_mode):
        self.__buffer_size = buffer_size
        self.__selection_mode = is_selection_mode

    def save_expression(self, node):
        if self.__buffer_size() == 0:
            raise EmptySelectionOrCriteriaSException(
                "Unable to save empty " + "selection" if self.__selection_mode() else "criteria")
