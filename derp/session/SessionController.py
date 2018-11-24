"""
SessionController.py

Class definition for the SessionController object.
"""
import derp.language as language
from derp.exceptions import *

from .Evaluator import Evaluator
from .ISessionController import ISessionController
from .SessionAction import SessionAction, SessionActionType, SessionActionModeType
from .UXAction import UXAction, UXActionType, UXActionModeType
from .session_state import *
from derp.selections.execution import *

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

    def __init__(self, selection_executor_factory, module_controller, file_manager):
        # external dependencies
        self.__module_controller = module_controller

        # type: SelectionExecutorFactory
        self.__selection_executor_factory = selection_executor_factory

        # type: SessionStateController
        self.__session_state = SessionStateController(file_manager)

        # other members
        self.__main_mode_parser = language.Parser(
            language.grammars.main_grammar())

        self.__selection_mode_parser = language.Parser()
        self.__criteria_mode_parser = language.Parser()

        # Set up the transformer. Requires a few helper functions to communicate with the
        # rest of the system.
        def load_asts(criteria_or_selection_name):
            asts = []

            assert self.__session_state.criteria_exists(
                criteria_or_selection_name) or self.__session_state.selection_exists(criteria_or_selection_name)

            lines = None
            parser = None

            if self.__session_state.criteria_exists(criteria_or_selection_name):
                lines = self.__session_state.load_criteria(
                    criteria_or_selection_name)
                parser = self.__criteria_mode_parser
            else:
                lines = self.__session_state.load_selection(
                    criteria_or_selection_name)
                parser = self.__selection_mode_parser

            for line in lines:
                line_ast = parser.parse(line)
                line_ast = self.__transformer.transform(line_ast)
                self.__semantic_check.check(line_ast)
                asts.append(line_ast)
            return asts

        def get_loaded_fields():
            fields = []
            for module in self.__module_controller.loaded_modules():
                definition = module.post_definition()
                fields.append(list(definition.field_definitions.keys()))
            return fields

        self.__transformer = language.Transformer(
            load_asts,
            lambda criteria_name: self.__session_state.criteria_exists(
                criteria_name),
            lambda selection_name: self.__session_state.selection_exists(
                selection_name)
        )

        self.__semantic_check = language.SemanticChecker(get_loaded_fields,
            lambda criteria_name: self.__session_state.criteria_exists(
                criteria_name),
            lambda selection_name: self.__session_state.selection_exists(
                selection_name),
            lambda module_name: self.__module_controller.module_is_registered(
                module_name),
            lambda module_name: self.__module_controller.module_is_loaded(
                module_name),
            lambda: len(self.__module_controller.loaded_modules()) != 0,
            lambda: self.__current_mode == self.SessionModeType.SELECTION,
            lambda: len(self.__session_state.get_buffer().get_commands()))

        self.__evaluator = Evaluator()

        # keep the latest line of input on hand in case it is needed while
        # handling a session action. Mainly used to append the current input to the buffer
        # during criteria/ selection creation.
        self.__last_input = None

        # session action handling dictionary
        self.__action_handling = {
            SessionActionType.QUERY: self._read_operation,
            SessionActionType.LOAD_MODULE: self._load_operation,
            SessionActionType.UNLOAD_MODULE: self._unload_operation,
            SessionActionType.RECALL: self._recall_operation,
            SessionActionType.CHANGE_MODE: self._change_mode_operation,
            SessionActionType.SAVE_BUFFER: self._save_buffer_operation,
            SessionActionType.APPEND_TO_BUFFER: self._append_to_buffer_operation,
            SessionActionType.NOOP: self._no_op_operation,
            SessionActionType.CLEAR_BUFFER: self._clear_operation
        }

        # Initialize in main mode
        self._switch_to_main_mode()

    def _recall_operation(self, session_action):
        # In main mode, there's not something in the buffer that needs
        # to persist, so load up the thing that was requested into the buffer
        if self.__current_mode == self.SessionModeType.MAIN:
            assert(session_action.get_data() is not None)
            target_name = session_action.get_data()

            # Already verified by semantic checker
            assert self.__session_state.criteria_exists(
                target_name) or self.__session_state.selection_exists(target_name)

            try:
                if self.__session_state.criteria_exists(target_name):
                    lines = self.__session_state.load_criteria(target_name)
                else:
                    lines = self.__session_state.load_selection(target_name)
            except FileIOException as e:
                action = UXAction(UXActionType.ERROR, e)
                return action

            assert lines is not None

            action = UXAction(UXActionType.RECALL, lines,
                              session_action.get_warnings())
            return action

        else:
            list_commands = self.__session_state.get_buffer().get_commands()
            action = UXAction(UXActionType.RECALL, list_commands,
                              session_action.get_warnings())
            return action

    def _read_operation(self, session_action):
        # In main mode, there's not something in the buffer that needs
        # to persist, so load up the thing that was requested into the buffer
        if self.__current_mode == self.SessionModeType.MAIN:
            assert(session_action.get_data() is not None)
            target_name = session_action.get_data()

            # Already verified by the semantic check
            assert self.__session_state.selection_exists(target_name)

            try:
                list_commands = self.__session_state.load_selection(
                    target_name)
            except FileIOException as e:
                action = UXAction(UXActionType.ERROR, e)
                return action
        else:
            list_commands = self.__session_state.get_buffer().get_commands()

        assert list_commands is not None

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
            assert False

        action = UXAction(ux_action, ux_mode,
                          warnings=session_action.get_warnings())
        return action

    def _perform_query(self, lines):
        ast_list = []
        for line in lines:
            ast = self.__selection_mode_parser.parse(line)
            ast = self.__transformer.transform(ast)
            self.__semantic_check.check(ast)
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
        except DerpException as e:
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

        # Last module was just unloaded
        if len(active_modules) == 0:
            self.__criteria_mode_parser = language.Parser()
            self.__selection_mode_parser = language.Parser()

        # Merge all grammars from loaded modules
        else:

            # TODO enforce that source grammars are valid
            try:
                field_grammars = [module.post_definition().field_grammar()
                                  for module in active_modules]
                source_grammars = [(module.name(), module.source_grammar(),)
                                   for module in active_modules]

                # Build a list of all the {modulename}_source rules
                # that exist
                source_productions = []
                for name, grammar in source_grammars:
                    # Module grammars must not define a start symbol
                    assert(grammar.start_symbol() is None)

                    # Do all text matching with lower case
                    name_source = name.lower() + "_source"
                    grammar_source = None

                    # Find the grammar rule that is {modulename}_source
                    # It can be all caps (token) or all lower case (rule), and may begin with !
                    for key, productions in grammar.productions():
                        alnum_key = ''.join(
                            x if x.isalnum() or x == '_' else '' for x in key.lower())

                        if name_source == alnum_key:
                            grammar_source = key

                    assert(grammar_source is not None)
                    source_productions.append(
                        grammar_source + " -> source_module")

                assert(len(source_productions) > 0)

                # Make a grammar that is just the rule 'source -> [each module source name]'
                source_rule_grammar = language.Grammar(
                    {'source': source_productions}
                )

                source_grammars = [module.source_grammar()
                                   for module in active_modules]

                self.__criteria_mode_parser = language.Parser(
                    language.grammars.criteria_grammar(),
                    *field_grammars,
                    *source_grammars,
                    source_rule_grammar
                )
                self.__selection_mode_parser = language.Parser(
                    language.grammars.selection_grammar(),
                    *field_grammars,
                    *source_grammars,
                    source_rule_grammar
                )
            except DerpException as e:
                raise e

    def _save_buffer_operation(self, save_action):
        assert(save_action.get_data() is not None)
        new_name = save_action.get_data()

        try:
            if self.__current_mode == self.SessionModeType.CRITERIA:
                self.__session_state.save_criteria(new_name)
            elif self.__current_mode == self.SessionModeType.SELECTION:
                self.__session_state.save_selection(new_name)
            else:
                assert False
        except FileIOException as e:
            action = UXAction(UXActionType.ERROR, e)
            return action

        return self._no_op_operation(save_action)

    def _append_to_buffer_operation(self, append_action):
        self.__session_state.get_buffer().add_command(self.__last_input)
        return self._no_op_operation(append_action)

    def _clear_operation(self, clear_action):
        if self.__current_mode == self.SessionModeType.MAIN:
            assert (clear_action.get_data() is not None)
            target_name = clear_action.get_data()

            # Already verified by the semantic check
            assert self.__session_state.criteria_exists(
                target_name) or self.__session_state.selection_exists(target_name)

            try:
                if self.__session_state.criteria_exists(
                        target_name):
                    self.__session_state.delete_criteria(target_name)
                else:
                    self.__session_state.delete_selection(target_name)
            except FileIOException as e:
                action = UXAction(UXActionType.ERROR, e)
                return action
        else:
            self.__session_state.get_buffer().clear()

        action = UXAction(UXActionType.NO_OP, None)
        return action

    def _switch_to_main_mode(self):
        self.__current_mode = self.SessionModeType.MAIN
        self.__parser_controller = self.__main_mode_parser
        self.__session_state.get_buffer().clear()

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
            ast = self.__parser_controller.parse(string_input)
            ast = self.__transformer.transform(ast)
            self.__semantic_check.check(ast)
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
