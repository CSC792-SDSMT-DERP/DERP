"""
derp.py

Responsible for constructing the Repl, PostReader, SessionController, SelectionExecutorFactory,
ModuleController, and Module objects on startup. Performs any required dependency injection as necessary.
"""
from derp.modules import ModuleController
from derp.session import SessionController
from derp.session.session_state import FileManager
from derp.exceptions import ModuleInitializationException, ModuleDefinitionException
from derp.selections.execution import SelectionExecutorFactory
from frontend import Repl, PostReader

from derp.session.tests.mock_module import MockModule
from modules import RedditModule

import json


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
    try:
        module_controller.register_module(mock_module)
    except ModuleDefinitionException as e:
        print("Mock module is does not meet module API")

    reddit_creds_json = open("reddit_credentials.json", "r")
    reddit_creds = json.load(reddit_creds_json)

    """
    At minimum, reddit_credentials.json must contain
    {
        "client_id": "[client id string]",
        "client_secret": "[client secret string]",
        "user_agent":"[user agent string]"
    }

    It may optionally provide
    {
        "username": "",
        "password": ""
    }
    """

    try:
        reddit_module = RedditModule(**reddit_creds)
        module_controller.register_module(reddit_module)
    except ModuleInitializationException as e:
        print("Failed to load reddit module: ", e)
    except ModuleDefinitionException as e:
        print("Reddit module is does not meet module API")

    repl.read_eval_print_loop()


if __name__ == "__main__":
    main()
