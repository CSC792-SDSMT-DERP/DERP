"""
ModuleController.py

Class definition for the ModuleController object.
"""

from derp.exceptions import *

from .IModuleController import IModuleController
from .tests.IModule_tests import TestIModule


class ModuleController(IModuleController):
    """
    The ModuleController is responsible for managing modules that are loaded, and for exposing
    loaded modules to the rest of the DERP backend.
    """

    def __init__(self):
        self.__modules = {}
        self.__active_modules = set([])

    def get_posts(self, source_ast, qualifier_tree):
        """
        Dispatches a query to the module which handles the sources specified in the source_ast.
        :param source_ast: A source_ast handled entirely by a single module.
        :param qualifier_tree: A tree representing a logical expression which the posts must match.
        :return: a PostIterator which iterates over the returned set of posts
        :raises ModuleNotLoadedException: module queried is not loaded
        """
        assert(source_ast.data == "source_module")

        module_name = source_ast.children[0].lower()
        module_source_ast = source_ast.children[1]

        if not self.module_is_loaded(module_name):
            raise ModuleNotLoadedException(
                "Module " + module_name + " not loaded")

        return self.__modules[module_name].get_posts(
            module_source_ast, qualifier_tree)

    def register_module(self, module):
        """
        Adds a module to the module registry, making it eligible for loading.
        :raises ModuleRegistrationException: raised if a module is already registered with a given name
        :raises ModuleDefinitionException: raised if the module is malformed
        :param module: A derp.module.IModule to register
        """

        if not TestIModule().module_is_valid(module):
            raise ModuleDefinitionException(
                "Module does not pass IModule tests")

        module_name = module.name().lower()
        if module_name in self.__modules:
            raise ModuleRegistrationException(
                "Module " + module_name + " registered twice")

        self.__modules[module_name] = module

    def module_is_registered(self, name):
        """
        Checks if a module is registered, regardless of if it is loaded
        :param name: name of the module to check for
        """
        return name.lower() in self.__modules

    def module_is_loaded(self, name):
        """
        Checks if a module is loaded
        :param name: name of the module to check for
        """
        return name.lower() in self.__active_modules

    def load_module(self, name):
        """
        Marks a module as active in the module registry.
        :raises ModuleNotRegisteredException: raised if the module is not registered
        :param name: name of the module to load
        :type name: str
        """
        module_name = name.lower()
        if module_name not in self.__modules:
            raise ModuleNotRegisteredException(
                "Module " + module_name + " not registered")

        self.__active_modules.add(module_name)

    def unload_module(self, name):
        """
        Marks a module as inactive in the module registry.
        :raises ModuleNotLoadedException: raised if the module is not currently active in the module registry.
        :param name: name of the module to unload
        :type name: str
        """
        module_name = name.lower()
        if module_name not in self.__active_modules:
            raise ModuleNotLoadedException(
                "Module " + module_name + " not loaded")

        self.__active_modules.remove(module_name)

    def loaded_modules(self):
        """
        Retrieves a list of all of the actively loaded modules.
        :return: a list of all of the actively loaded modules
        """
        return [self.__modules[name] for name in self.__active_modules]
