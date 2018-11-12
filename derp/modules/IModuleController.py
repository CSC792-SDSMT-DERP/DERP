"""
IModuleController.py

Interface definition for ModuleController objects.
"""

from derp.modules.IPostQueryable import IPostQueryable


class IModuleController(IPostQueryable):
    """
    A ModuleController is required to be able to load and unload modules, and manage loaded modules.
    It also dispatches queries to the appropriate loaded modules.
    """

    def register_module(self, module):
        """
        Adds a module to the module registry, making it eligible for loading.
        :raises ModuleRegistrationException: raised if a module is already registered with a given name
        :raises ModuleDefinitionException: raised if the module is malformed
        :param module: A derp.module.IModule to register
        """
        pass

    def load_module(self, name):
        """
        Marks a module as active in the module registry.
        :raises ModuleNotRegisteredException: raised if the module is not registered
        :param name: name of the module to load
        :type name: str
        """
        pass

    def unload_module(self, name):
        """
        Marks a module as inactive in the module registry.
        :raises ModuleNotLoadedException: raised if the module is not currently active in the module registry.
        :param name: name of the module to unload
        :type name: str
        """
        pass

    def loaded_modules(self):
        """
        Retrieves a list of all of the actively loaded modules.
        :return: a list of all of the actively loaded modules
        """
        pass
