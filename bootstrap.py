"""
bootstrap.py

Responsible for constructing the Repl, PostReader, SessionController, SelectionExecutorFactory,
ModuleController, and Module objects on startup. Performs any required dependency injection as necessary.
"""
from derp.modules.ModuleController import ModuleController
from derp.session.SessionController import SessionController
from derp.session.selection_execution.SelectionExecutorFactory import SelectionExecutorFactory
from frontend.Repl import Repl
from frontend.PostReader import PostReader
from modules.reddit.RedditModule import RedditModule


def main():
    """
    Performs on-start setup for the DERP interpreter including
    core object construction and pre-requisite setup for default modules
    :return: None
    """
    module_controller = ModuleController()
    post_reader = PostReader()
    selection_executor_factory = SelectionExecutorFactory(module_controller)
    session_controller = SessionController(selection_executor_factory, module_controller)
    repl = Repl(session_controller, post_reader)

    # TODO: replace with register module.
    # set module_controller dependencies
    module_controller.load_module("RedditModule")

    repl.read_eval_print_loop()


if __name__ == "__main__":
    main()
