"""
SessionController.py

Class definition for the SessionController object.
"""
from derp.language.Parser import Parser
from derp.language.Transformer import Transformer
from derp.session.Evaluator import Evaluator
from derp.session.ISessionController import ISessionController
from derp.session.session_state.FileManager import FileManager
from derp.session.session_state.SessionStateController import SessionStateController


class SessionController(ISessionController):
    """
    The SessionController acts as the master object for the backend. It is
    responsible for receiving user input from the Repl and generating UXActions
    to send back to the Repl. Additionally, the SessionController manages the
    parsing and evaluation pipeline, and manages selection and criterion persistence.
    """

    def __init__(self):
        # external dependencies
        self.__repl = None
        self.__module_controller = None

        # other members
        self.__parser_controller = Parser()
        self.__transformer = Transformer()
        self.__evaluator = Evaluator()
        self.__session_state = SessionStateController()
        self.__storage_persistence = FileManager()

    def set_repl(self, repl):
        self.__repl = repl

    def set_module_controller(self, module_controller):
        self.__module_controller = module_controller

    def run_input(self, string_input):
        """
        The SessionController provides responses to strings of input
        representing DERP language constructs.
        :param string_input: a line of user input
        :return: UXAction instructing the Repl how to proceed
        """
        pass
