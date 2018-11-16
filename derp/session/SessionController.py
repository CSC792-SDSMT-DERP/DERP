"""
SessionController.py

Class definition for the SessionController object.
"""
from derp.language.Parser import Parser
from derp.language.Transformer import Transformer
from derp.session.Evaluator import Evaluator
from derp.session.ISessionController import ISessionController
from derp.session.SessionAction import SessionAction, SessionActionType
from derp.session.UXAction import UXAction, UXActionType
from derp.session.session_state.FileManager import FileManager
from derp.session.session_state.SessionStateController import SessionStateController
from derp.session.selection_execution.SelectionExecutorFactory import SelectionExecutorFactory
from derp.exceptions.exceptions import ModuleNotLoadedException, ModuleNotRegisteredException, TextParseException
from derp.language.GrammarLibrary import *


class SessionController(ISessionController):
    """
    The SessionController acts as the master object for the backend. It is
    responsible for receiving user input from the Repl and generating UXActions
    to send back to the Repl. Additionally, the SessionController manages the
    parsing and evaluation pipeline, and manages selection and criterion persistence.
    """

    def __init__(self, selection_executor_factory, module_controller):
        # external dependencies
        self.__module_controller = module_controller
        self.__selection_executor_factory = selection_executor_factory  # type: SelectionExecutorFactory

        # other members
        self.__parser_controller = Parser()
        self.__transformer = Transformer()
        self.__evaluator = Evaluator()
        self.__session_state = SessionStateController()
        self.__file_manager = FileManager()

        # Load main mode grammar
        self.__parser_controller.set_grammar(MAIN_MODE_GRAMMAR)

        # session action handling dictionary
        self.__action_handling = {
            SessionActionType.QUERY: self._read_operation,
            SessionActionType.LOAD_MODULE: self._load_operation,
            SessionActionType.UNLOAD_MODULE: self._unload_operation
        }

    def _recall_operation(self, session_action):
        list_commands = self.__session_state.get_buffer().get_commands()
        action = UXAction(UXActionType.RECALL, list_commands, session_action.get_warnings())
        return action

    def _read_operation(self, session_action):
        executor = self._perform_query(session_action.get_file_name())
        action = UXAction(UXActionType.READ, executor, session_action.get_warnings())
        return action

    def _no_op_operation(self, session_action):
        action = UXAction(UXActionType.NO_OP, warnings=session_action.get_warnings())
        return action

    def _change_mode_operation(self, session_action):
        action = UXAction(UXActionType.CHANGE_MODE, session_action.get_data(), warnings=session_action.get_warnings())
        return action

    def _perform_query(self, name):
        lines = self.__file_manager.read_file(name)
        ast_list = []
        for line in lines:
            ast = self.__parser_controller.parse(line)
            ast = self.__transformer.transform(ast)
            ast_list.append(ast)
        executor = self.__selection_executor_factory.build_selection_executor(ast_list)
        return executor

    def _load_operation(self, load_action):
        module_name = load_action.get_data()
        try:
            self.__module_controller.load_module(module_name)
            active_modules = self.__module_controller.loaded_modules()
            field_grammars = [module.post_definition().field_grammar() for module in active_modules]
            source_grammars = [module.source_grammar() for module in active_modules]
            # TODO: Merge grammars and roll back on failure
        except ModuleNotRegisteredException as e:
            return UXAction(UXActionType.ERROR, e)
        return self._no_op_operation(load_action)

    def _unload_operation(self, unload_action):
        module_name = unload_action.get_data()
        try:
            self.__module_controller.unload_module(module_name)
            active_modules = self.__module_controller.loaded_modules()
            field_grammars = [module.post_definition().field_grammar() for module in active_modules]
            source_grammars = [module.source_grammar() for module in active_modules]
            # TODO: Merge grammars (failure should never happen)
        except ModuleNotLoadedException as e:
            return UXAction(UXActionType.ERROR, e)
        return self._no_op_operation(unload_action)

    def run_input(self, string_input):
        """
        The SessionController provides responses to strings of input
        representing DERP language constructs.
        :param string_input: a line of user input
        :return: UXAction instructing the Repl how to proceed
        """
        try:
            ux_action = None
            # TODO: maintain three separate parsers and a mode tracker
            ast = self.__parser_controller.parse(string_input)
            ast = self.__transformer.transform(ast)
            # TODO: evaluator currently returns nothing
            session_action = self.__evaluator.evaluate(ast)  # type: SessionAction

            ux_action = self.__action_handling[session_action.get_type()](session_action)
            return ux_action
        except TextParseException as e:
            return UXAction(UXActionType.ERROR, e)



