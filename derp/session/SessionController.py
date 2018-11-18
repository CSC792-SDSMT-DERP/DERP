"""
SessionController.py

Class definition for the SessionController object.
"""
from derp.language.Parser import Parser
from derp.language.Transformer import Transformer
from derp.session.Evaluator import Evaluator
from derp.session.ISessionController import ISessionController
from derp.session.SessionAction import SessionAction, SessionActionType, SessionActionModeType
from derp.session.UXAction import UXAction, UXActionType, UXActionModeType
from derp.session.session_state.FileManager import FileManager
from derp.session.session_state.SessionStateController import SessionStateController
from derp.session.selection_execution.SelectionExecutorFactory import SelectionExecutorFactory
from derp.exceptions.exceptions import *
from derp.language.GrammarLibrary import *

from enum import Enum


class SessionController(ISessionController):
    """
    The SessionController acts as the master object for the backend. It is
    responsible for receiving user input from the Repl and generating UXActions
    to send back to the Repl. Additionally, the SessionController manages the
    parsing and evaluation pipeline, and manages selection and criterion persistence.
    """
    class SessionModeType(Enum):
        MAIN = 1
        SELECTION = 2
        CRITERIA = 3

    def __init__(self, selection_executor_factory, module_controller):
        # external dependencies
        self.__module_controller = module_controller

        # type: SelectionExecutorFactory
        self.__selection_executor_factory = selection_executor_factory

        # other members
        self.__main_mode_parser = Parser(MAIN_MODE_GRAMMAR)
        self.__selection_mode_parser = Parser()
        self.__criteria_mode_parser = Parser()

        self.__transformer = Transformer()
        self.__evaluator = Evaluator()
        self.__session_state = SessionStateController(FileManager())

        # Initialize in main mode
        self._switch_to_main_mode()

        # session action handling dictionary
        self.__action_handling = {
            SessionActionType.QUERY: self._read_operation,
            SessionActionType.LOAD_MODULE: self._load_operation,
            SessionActionType.UNLOAD_MODULE: self._unload_operation,
            SessionActionType.RECALL: self._recall_operation,
            SessionActionType.CHANGE_MODE: self._change_mode_operation,
            SessionActionType.SAVE_BUFFER: self._save_buffer_operation,
            SessionActionType.APPEND_TO_BUFFER: self._append_to_buffer_operation,

            # todo because clear x is main mode but possible right now
            SessionActionType.CLEAR_BUFFER: self._clear_buffer_operation
        }

    def _recall_operation(self, session_action):
        # In main mode, there's not something in the buffer that needs
        # to persist, so load up the thing that was requested into the buffer
        if(self.__current_mode == self.SessionModeType.MAIN):
            assert(session_action.get_data() is not None)
            target_name = session_action.get_data()

            # TODO : Handle if this is criteria or selection
            # TODO : Handle if this fails, because filesystems
            self.__session_state.load_criteria(target_name)

        list_commands = self.__session_state.get_buffer().get_commands()
        action = UXAction(UXActionType.RECALL, list_commands,
                          session_action.get_warnings())
        return action

    def _read_operation(self, session_action):
        # In main mode, there's not something in the buffer that needs
        # to persist, so load up the thing that was requested into the buffer
        if(self.__current_mode == self.SessionModeType.MAIN):
            assert(session_action.get_data() is not None)
            target_name = session_action.get_data()

            # TODO : Handle if this fails, because filesystems
            self.__session_state.load_selection(target_name)

        list_commands = self.__session_state.get_buffer().get_commands()
        executor = self._perform_query(list_commands)

        action = UXAction(UXActionType.READ, executor,
                          session_action.get_warnings())
        return action

    def _no_op_operation(self, session_action):
        action = UXAction(UXActionType.NO_OP,
                          warnings=session_action.get_warnings())
        return action

    def _change_mode_operation(self, session_action):
        assert(session_action.get_data() is not None)
        target_switch = session_action.get_data()
        ux_mode = None
        ux_action = UXActionType.CHANGE_MODE

        if target_switch == SessionActionModeType.EXIT:
            if self.__current_mode == self.SessionModeType.MAIN:
                ux_mode = None
                ux_action = UXActionType.EXIT
            else:
                self._switch_to_main_mode()
                ux_mode = UXActionModeType.MAIN
        elif target_switch == SessionActionModeType.SELECTION:
            self._switch_to_selection_mode()
            ux_mode = UXActionModeType.SELECTION
        elif target_switch == SessionActionModeType.CRITERIA:
            self._switch_to_criteria_mode()
            ux_mode = UXActionModeType.CRITERIA
        else:
            assert(False)

        action = UXAction(ux_action, ux_mode,
                          warnings=session_action.get_warnings())
        return action

    def _perform_query(self, lines):
        ast_list = []
        for line in lines:
            ast = self.__selection_mode_parser.parse(line)
            ast = self.__transformer.transform(ast)
            ast_list.append(ast)

        executor = self.__selection_executor_factory.build_selection_executor(
            ast_list)
        return executor

    def _load_operation(self, load_action):
        module_name = load_action.get_data()
        try:
            self.__module_controller.load_module(module_name)
        except ModuleNotRegisteredException as e:
            return UXAction(UXActionType.ERROR, e)

        try:
            self._build_selection_and_criteria_grammars()
        except Exception as e:
            self.__module_controller.unload_module(module_name)
            return UXAction(UXActionType.ERROR, e)

        return self._no_op_operation(load_action)

    def _unload_operation(self, unload_action):
        module_name = unload_action.get_data()

        # TODO remove this try catch by providing a way to get it in
        # the semantic checker
        try:
            self.__module_controller.unload_module(module_name)
        except ModuleNotLoadedException as e:
            return UXAction(UXActionType.ERROR, e)

        self._build_selection_and_criteria_grammars()
        return self._no_op_operation(unload_action)

    def _build_selection_and_criteria_grammars(self):
        active_modules = self.__module_controller.loaded_modules()

        # TODO enforce that source grammars are valid
        try:
            field_grammars = [module.post_definition().field_grammar()
                              for module in active_modules]
            source_grammars = [module.source_grammar()
                               for module in active_modules]

            self.__criteria_mode_parser = Parser(CRITERIA_MODE_GRAMMAR, *field_grammars, *source_grammars)
            self.__selection_mode_parser = Parser(SELECTION_MODE_GRAMMAR, *field_grammars, *source_grammars)
        except GrammarMergeException as e:
            raise e
        except GrammarDefinitionException as e:
            raise e
        except Exception as e:
            raise ModuleDefinitionException() from e

    def _save_buffer_operation(self, save_action):
        assert(save_action.get_data() is not None)
        new_name = save_action.get_data()

        if self.__current_mode == self.SessionModeType.CRITERIA:
            self.__session_state.save_criteria(new_name)
        elif self.__current_mode == self.SessionModeType.SELECTION:
            self.__session_state.save_selection(new_name)
        else:
            assert(False)
        return self._no_op_operation(save_action)

    def _append_to_buffer_operation(self, append_action):
        self.__session_state.get_buffer().add_command(self.__last_input)
        return self._no_op_operation(append_action)

    def _clear_buffer_operation(self, clear_action):
        return self._no_op_operation(clear_action)

    def _switch_to_main_mode(self):
        self.__current_mode = self.SessionModeType.MAIN
        self.__parser_controller = self.__main_mode_parser

    def _switch_to_criteria_mode(self):
        self.__current_mode = self.SessionModeType.CRITERIA
        self.__parser_controller = self.__criteria_mode_parser

    def _switch_to_selection_mode(self):
        self.__current_mode = self.SessionModeType.SELECTION
        self.__parser_controller = self.__selection_mode_parser

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
            session_action = self.__evaluator.evaluate(
                ast)  # type: SessionAction

            self.__last_input = string_input
            ux_action = self.__action_handling[session_action.get_type()](
                session_action)
            return ux_action
        except TextParseException as e:
            return UXAction(UXActionType.ERROR, e)
        except SemanticException as e:
            return UXAction(UXActionType.ERROR, e)
