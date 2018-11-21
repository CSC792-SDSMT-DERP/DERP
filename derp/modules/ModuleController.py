"""
ModuleController.py

Class definition for the ModuleController object.
"""

from derp.exceptions import ModuleRegistrationException, ModuleNotRegisteredException, ModuleNotLoadedException

from .IModuleController import IModuleController


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
        """
        # TODO: I'm not sure how the source ast will be parsed at the moment
        pass

    def register_module(self, module):
        """
        Adds a module to the module registry, making it eligible for loading.
        :raises ModuleRegistrationException: raised if a module is already registered with a given name
        :raises ModuleDefinitionException: raised if the module is malformed
        :param module: A derp.module.IModule to register
        """

        # TODO: Find a way to enforce IModule on the module and raise ModuleDefinitionException if needed

        if module.name() in self.__modules:
            raise ModuleRegistrationException(
                "Module " + module.name() + " registered twice")

        self.__modules[module.name()] = module

    def module_is_registered(self, name):
        """
        Checks if a module is registered, regardless of if it is loaded
        :param name: name of the module to check for
        """
        return name in self.__modules

    def module_is_loaded(self, name):
        """
        Checks if a module is loaded
        :param name: name of the module to check for
        """
        return name in self.__active_modules

    def load_module(self, name):
        """
        Marks a module as active in the module registry.
        :raises ModuleNotRegisteredException: raised if the module is not registered
        :param name: name of the module to load
        :type name: str
        """
        if name not in self.__modules:
            raise ModuleNotRegisteredException(
                "Module " + name + " not registered")

        self.__active_modules.add(name)

    def unload_module(self, name):
        """
        Marks a module as inactive in the module registry.
        :raises ModuleNotLoadedException: raised if the module is not currently active in the module registry.
        :param name: name of the module to unload
        :type name: str
        """
        # TODO : Is this really an exception?
        if name not in self.__active_modules:
            raise ModuleNotLoadedException("Module " + name + " not loaded")

        self.__active_modules.remove(name)

    def loaded_modules(self):
        """
        Retrieves a list of all of the actively loaded modules.
        :return: a list of all of the actively loaded modules
        """
        return [self.__modules[name] for name in self.__active_modules]
