"""
ModuleController.py

Class definition for the ModuleController object.
"""
import typing  # TODO: remove when development is done

from derp.modules.IModule import IModule  # TODO: remove when development is done
from derp.modules.IModuleController import IModuleController


class ModuleController(IModuleController):
    """
    The ModuleController is responsible for managing modules that are loaded, and for exposing
    loaded modules to the rest of the DERP backend.
    """

    def __init__(self):
        self.__modules = []  # type: typing.List[IModule]

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
