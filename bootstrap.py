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
    post_reader = PostReader()
    repl = Repl()
    session_controller = SessionController()
    selection_executor_factory = SelectionExecutorFactory()
    module_controller = ModuleController()

    # set repl dependencies
    repl.set_post_reader(post_reader)
    repl.set_session_controller(session_controller)

    # set post_reader dependencies
    post_reader.set_repl(repl)

    # set session_controller dependencies
    session_controller.set_repl(repl)
    session_controller.set_selection_executor_factory(selection_executor_factory)
    session_controller.set_module_controller(module_controller)

    # set selection_executor_factory dependencies
    selection_executor_factory.set_module_controller(module_controller)

    # set module_controller dependencies
    module_controller.load_module("RedditModule")

    repl.read_eval_print_loop()


if __name__ == "__main__":
    main()
