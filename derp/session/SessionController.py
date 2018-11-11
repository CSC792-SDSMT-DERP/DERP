"""
SessionController.py

Class definition for the SessionController object.
"""
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

        # other members
        self.__parser_controller = ParserController()
        self.__transformer = Transformer()
        self.__evaluator = Evaluator()
        self.__session_state = SessionStateController()
        self.__storage_persistence = FileManager()

    def set_repl(self, repl):
        self.__repl = repl
