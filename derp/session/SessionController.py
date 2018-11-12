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
        self.__selection_executor_factory = None  # type: SelectionExecutorFactory

        # other members
        self.__parser_controller = Parser()
        self.__transformer = Transformer()
        self.__evaluator = Evaluator()
        self.__session_state = SessionStateController()
        self.__file_manager = FileManager()

        # session action handling dictionary
        self.__action_handling = {
            SessionActionType.QUERY: self._read_operation
        }

    def set_repl(self, repl):
        self.__repl = repl

    def set_selection_executor_factory(self, selection_executor_factory):
        self.__selection_executor_factory = selection_executor_factory

    def set_module_controller(self, module_controller):
        self.__module_controller = module_controller

    def _recall_operation(self,session_action):
        list_commands = self.__session_state.get_buffer().get_commands()
        output = " ".join(list_commands)
        action = UXAction(UXActionType.RECALL, text=output, warnings=session_action.get_warnings())
        return action

    def _read_operation(self, session_action):
        executor = self._perform_query(session_action.get_file_name())
        action = UXAction(UXActionType.READ, post_iterator=executor, warnings=session_action.get_warnings())
        return action

    def _no_op_operation(self, session_action):
        action = UXAction(UXActionType.NO_OP, warnings=session_action.get_warnings())
        return action

    def _change_mode_operation(self, session_action):
        action = UXAction(UXActionType.CHANGE_MODE, text=session_action.get_text(), warnings=session_action.get_warnings())
        return action

    def _error_operation(self, session_action):
        action = UXAction(UXActionType.ERROR, text=session_action.get_text(), warnings=session_action.get_warnings())
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

    def run_input(self, string_input):
        """
        The SessionController provides responses to strings of input
        representing DERP language constructs.
        :param string_input: a line of user input
        :return: UXAction instructing the Repl how to proceed
        """
        ux_action = None
        ast = self.__parser_controller.parse(string_input)
        ast = self.__transformer.transform(ast)  # TODO: this is currently based off a local stub and may be inaccurate
        # TODO: evaluator currently returns nothing
        session_action = self.__evaluator.evaluate(ast)  # type: SessionAction

        ux_action = self.__action_handling[session_action.get_type()](session_action)

        return ux_action
