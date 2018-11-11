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


def create_objects():
    post_reader = PostReader()
    repl = Repl()
    session_controller = SessionController()
    selection_executor_factory = SelectionExecutorFactory()
    module_controller = ModuleController()
    module = RedditModule()

    # set repl dependencies
    repl.set_post_reader(post_reader)
    repl.set_session_controller(session_controller)

    # set post_reader dependencies
    post_reader.set_repl(repl)

    # set session_controller dependencies
    session_controller.set_repl(repl)

    return repl


def main():
    """
    Performs on-start setup for the DERP interpreter including
    core object construction and pre-requisite setup for default modules
    :return: None
    """
    pass


if __name__ == "__main__":
    main()
