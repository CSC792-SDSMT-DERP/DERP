from derp.modules import ModuleController
from derp.session import SessionController
from derp.session.session_state.tests.MockFileManager import MockFileManager
from derp.selections.execution import SelectionExecutorFactory
from .mock_module import MockModule


def make():
    """
    Create an empty derp session which uses the mock file manager
    """
    module_controller = ModuleController()
    file_manager = MockFileManager()
    selection_executor_factory = SelectionExecutorFactory(module_controller)

    session_controller = SessionController(
        selection_executor_factory, module_controller, file_manager)

    mock_module = MockModule()
    module_controller.register_module(mock_module)

    return session_controller
