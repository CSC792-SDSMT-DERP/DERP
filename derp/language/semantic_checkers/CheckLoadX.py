from lark import Visitor

from derp.exceptions import *


class CheckLoadX(Visitor):
    def __init__(self, module_exists, module_loaded):
        self.__module_exists = module_exists
        self.__module_loaded = module_loaded

    def load_expression(self, node):
        assert(len(node.children) == 1)

        module_name = node.children[0]

        if not self.__module_exists(module_name):
            raise MissingModuleSException(
                "Module '" + module_name + "' not found")

        if self.__module_loaded(module_name):
            raise ModuleAlreadyLoadedSException(
                "Module '" + module_name + "' is already loaded")
