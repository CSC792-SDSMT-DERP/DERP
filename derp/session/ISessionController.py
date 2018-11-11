"""
ISessionController.py

Interface definition for SessionController objects.
"""


class ISessionController:
    """
    ISessionControllers expose a method to handle lines of user input.
    """

    def run_input(self, string_input):
        """
        The SessionController provides responses to strings of input
        representing DERP language constructs.
        :param string_input: a line of user input
        :return: UXAction instructing the Repl how to proceed
        """
        pass
