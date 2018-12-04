def execute_and_check_derp_statements(sessioncontroller_impl, statements_and_checks):
    """
    Executes a sequence of derp statements in the given session implementation
    and asserts that, for each statement with result types given, the response matches the
    required response

    :param statements_and_checks: List of 1-tuple, 2-tuple, or 3-tuple with the first element a string
                                  If second element given, it is the UXActionType required
                                  If third element given, it is the data required in the Action get_data() or,
                                    if ActionType is Error, the type of Exception that should be given
    """

    from derp.session import UXActionType

    for command in statements_and_checks:
        print("Execute", command[0])
        result = sessioncontroller_impl.run_input(command[0])

        if len(command) > 1:
            print("Check action type is", command[1], result.get_type())
            assert command[1] == result.get_type()

        if len(command) > 2:
            if command[1] == UXActionType.ERROR:
                print("Check exception {0} is type".format(
                    result.get_data()), command[2])
                assert isinstance(result.get_data(), command[2])
            else:
                print("Check result data is", command[2], result.get_data())
                assert command[2] == result.get_data()
