"""
Repl.py

Class definition for the Repl object.
"""
from derp.exceptions import *
from derp.session import UXActionType, UXAction, SessionController, UXActionModeType
from .PostReader import PostReader

import os
import stat


def executing_a_file():
    mode = os.fstat(0).st_mode
    return stat.S_ISFIFO(mode) or stat.S_ISREG(mode)


class Repl:
    """
    The Repl handles IO operations for the backend by accepting UXActions
    generated by the SessionController. The Repl passes information to the
    SessionController as strings representing user input. The Repl is also
    responsible for passing an iterator to the ReadController when the user
    reads results of a query.
    """

    def __init__(self, session_controller, post_reader):
        self.__session_controller = session_controller  # type: SessionController
        self.__post_reader = post_reader  # type: PostReader
        self.__exiting = False
        self.__prompts = {
            UXActionModeType.MAIN: ">>> ",
            UXActionModeType.CRITERIA: "(criteria) >>> ",
            UXActionModeType.SELECTION: "(selection) >>> ",
        }
        self.__prompt = self.__prompts[UXActionModeType.MAIN]

        # UXAction handling dictionary
        self.__action_handling = {
            UXActionType.ERROR: self._handle_error,
            UXActionType.CHANGE_MODE: self._handle_change_mode,
            UXActionType.NO_OP: self._handle_no_op,
            UXActionType.RECALL: self._handle_recall,
            UXActionType.READ: self._handle_read,
            UXActionType.EXIT: self._handle_exit
        }

    def _handle_error(self, action):
        e = action.get_data()
        
        if isinstance(e, FileIOException):
            print("Failed to save/load a selection or criteria")
        elif isinstance(e, TextParseException):
            print("Invalid syntax, statement failed to parse")
        elif isinstance(e, GrammarMergeException):
            print("Attempt to merge grammars failed, module grammars are incompatible")
        elif isinstance(e, GrammarDefinitionException):
            print("Failed to define a grammar for the module")
        elif isinstance(e, SemanticException):
            print("Invalid semantics, statement was semantically incorrect")
        elif isinstance(e, ModuleDefinitionException):
            print("Module definition is invalid, failed to register module")
        elif isinstance(e, ModuleNotRegisteredException):
            print("An unregistered module was referenced")
        elif isinstance(e, ModuleNotLoadedException):
            print("An unloaded module was referenced")
        else:
            print(e)

    def _handle_change_mode(self, action):
        self.__prompt = self.__prompts[action.get_data()]

    def _handle_no_op(self, action):
        pass

    def _handle_recall(self, action):
        print("\n".join(action.get_data()))

    def _handle_read(self, action):
        self.__post_reader.read_from(action.get_data())

    def _print_warnings(self, action):
        warnings = action.get_warnings()
        if warnings is not None:
            for warning in warnings:
                print(warning)

    def _handle_input(self, string_input):
        """
        Handle a line of input by sending it to the SessionController
        :param string_input: A line of user input
        :type string_input: str
        :return: None
        """
        action = self.__session_controller.run_input(
            string_input)  # type: UXAction
        self.__action_handling[action.get_type()](action)

        self._print_warnings(action)

    def _handle_exit(self, action):
        self.__exiting = True

    def read_eval_print_loop(self):
        """
        Set the Repl object to reading from standard in until the program terminates
        :return: None
        """
        while not self.__exiting:
            try:
                string_input = input(self.__prompt)
                if executing_a_file():
                    print(string_input)

                self._handle_input(string_input)
            except EOFError as e:
                self.__exiting = True
                print("[EOF, exiting...]")
            except KeyboardInterrupt:
                self.__exiting = True
