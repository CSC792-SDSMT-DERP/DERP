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

    def load_module(self, name):
        """
        Loads a module with the given name and makes it available to the DERP backend.
        :raises ModuleDefinitionException: raised if the module is malformed
        :param name: name of the module to load
        :type name: str
        :return: boolean indicating success
        """
        pass

    def unload_module(self, name):
        """
        Unloads the module with the given name, removing its availability to the DERP backend.
        :param name: name of the module to unload
        :type name: str
        :return: boolean indicating success.
        """
        pass

