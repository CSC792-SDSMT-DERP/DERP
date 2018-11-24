from lark import Visitor

from derp.exceptions import SemanticException


class CheckCreateStatement(Visitor):
    def __init__(self, any_modules_loaded):
        self.__any_modules = any_modules_loaded

    def create_expression(self, node):
        if not self.__any_modules():
            raise SemanticException(
                "Cannot create a selection or criteria with no modules loaded")
