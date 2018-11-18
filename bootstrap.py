"""
bootstrap.py

Responsible for constructing the Repl, PostReader, SessionController, SelectionExecutorFactory,
ModuleController, and Module objects on startup. Performs any required dependency injection as necessary.
"""
from derp.modules.ModuleController import ModuleController
from derp.session.SessionController import SessionController
from derp.session.session_state.SessionStateController import SessionStateController
from derp.session.session_state.FileManager import FileManager
from derp.session.selection_execution.SelectionExecutorFactory import SelectionExecutorFactory
from frontend.Repl import Repl
from frontend.PostReader import PostReader
from modules.mock.MockModule import MockModule


def main():
    """
    Performs on-start setup for the DERP interpreter including
    core object construction and pre-requisite setup for default modules
    :return: None
    """
    module_controller = ModuleController()
    post_reader = PostReader()
    file_manager = FileManager()
    selection_executor_factory = SelectionExecutorFactory(module_controller)

    session_controller = SessionController(
        selection_executor_factory, module_controller, file_manager)

    repl = Repl(session_controller, post_reader)

    # For now, we explicitly register modules that we know exist,
    # in the future this could do discovery
    mock_module = MockModule()
    module_controller.register_module(mock_module)

    repl.read_eval_print_loop()


if __name__ == "__main__":
    main()
