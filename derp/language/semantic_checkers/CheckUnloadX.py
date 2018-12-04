from lark import Visitor

from derp.exceptions import *


class CheckUnloadX(Visitor):
    def __init__(self, module_loaded):
        self.__module_loaded = module_loaded

    def unload_expression(self, node):
        assert len(node.children) == 1

        module_name = node.children[0]

        if not self.__module_loaded(module_name):
            raise ModuleNotLoadedSException(
                "Module '" + module_name + "' is not loaded")
