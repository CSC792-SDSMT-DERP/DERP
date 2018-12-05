import pytest

from . import execute_and_check_derp_statements

from derp.session import UXActionType, UXActionModeType

from random import shuffle


@pytest.mark.slow
@pytest.mark.parallel
class TestMainModeBasicFunctionality:
    @pytest.mark.parametrize("command", ["exit", "stop"])
    def test_main_mode_can_exit(self, command, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [(command, UXActionType.EXIT)])

    def test_main_mode_can_load_module(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP, None,)])

    def test_main_mode_can_unload_module(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           ('unload "MockModule"', UXActionType.NO_OP, None,)])

    @pytest.mark.parametrize("type", [("criteria", UXActionModeType.CRITERIA),
                                      ("selection", UXActionModeType.SELECTION)])
    @pytest.mark.parametrize("command", ["create ",
                                         "create a ",
                                         "create new ",
                                         "create a new "])
    def test_can_enter_creation_modes(self, command, type, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           (command+type[0], UXActionType.CHANGE_MODE, type[1],)])


@pytest.mark.slow
@pytest.mark.parallel
class TestMainModeAdvancedFunctionality:
    @pytest.mark.parametrize("create_type,from_stmt", [("criteria", ""), ("selection", "from mock ")])
    def test_can_recall(self, create_type, from_stmt, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           ('create a new ' + create_type,),
                                           ('add posts ' + from_stmt +
                                            'with "hello world" in the title',),
                                           ('remove posts with a post date before November 2018',),
                                           ('save as "test"',),
                                           ('stop',),
                                           ('recall "test"', UXActionType.RECALL,
                                            ['add posts ' + from_stmt + 'with "hello world" in the title',
                                             'remove posts with a post date before November 2018'])])

    @pytest.mark.parametrize("create_type,from_stmt", [("criteria", ""), ("selection", "from mock ")])
    def test_can_clear(self, create_type, from_stmt, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           ('create a new ' + create_type,),
                                           ('add posts ' + from_stmt +
                                            'with "hello world" in the title',),
                                           ('remove posts with a post date before November 2018',),
                                           ('save as "test"',),
                                           ('stop',),
                                           ('clear "test"', UXActionType.NO_OP,)])

    @pytest.mark.parametrize("create_type,from_stmt", [("selection", "from mock ")])
    def test_can_read(self, create_type, from_stmt, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           ('create a new ' + create_type,),
                                           ('add posts ' + from_stmt +
                                            'with "hello world" in the title',),
                                           ('remove posts with a post date before November 2018',),
                                           ('save as "test"',),
                                           ('stop',),
                                           ('read "test"', UXActionType.READ,)])


@pytest.mark.slow
@pytest.mark.parallel
class TestCriteriaAndSelectionMode:
    def setup_class(self):
        self.__possible_qualifiers = ['with a post date before November 1018',
                                      'with "hello world" in the title',
                                      'which are not verified',
                                      'with the exact title "hello world"',
                                      'with over 100 points',
                                      'about "tests"',
                                      'matching "criteria"']

    @pytest.mark.parametrize("create_type,from_stmt", [("criteria", ""), ("selection", "from mock ")])
    def test_clear(self, create_type, from_stmt, sessioncontroller_impl):
        qualifier_string = self.__possible_qualifiers[0]

        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           ('add posts ' + from_stmt +
                                            qualifier_string, UXActionType.NO_OP,),
                                           ('clear', UXActionType.NO_OP,)])

    @pytest.mark.parametrize("create_type,from_stmt", [("criteria", ""), ("selection", "from mock ")])
    def test_recall(self, create_type, from_stmt, sessioncontroller_impl):
        qualifier_string = self.__possible_qualifiers[0]

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,),
                                           ('recall', UXActionType.RECALL, [add_line],)])

    @pytest.mark.parametrize("create_type,from_stmt", [("selection", "from mock ")])
    def test_read(self, create_type, from_stmt, sessioncontroller_impl):
        qualifier_string = self.__possible_qualifiers[0]

        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           ('add posts ' + from_stmt +
                                            qualifier_string, UXActionType.NO_OP,),
                                           ('read', UXActionType.READ,)])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('qualifier_bits', list(range(128)))
    def test_qualifier_statements(self, qualifier_bits, create_type, add_remove, from_stmt, sessioncontroller_impl):
        qualifiers = []
        for i in range(7):
            if (1 << i) & qualifier_bits:
                qualifiers.append(self.__possible_qualifiers[i])

        qualifier_string = ' and '.join(qualifiers)

        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new criteria',
                                            UXActionType.CHANGE_MODE,),
                                           ('add posts about "tests"',
                                            UXActionType.NO_OP,),
                                           ('save as "criteria"',
                                            UXActionType.NO_OP,),
                                           ('stop', UXActionType.CHANGE_MODE,
                                            UXActionModeType.MAIN,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_remove + ' posts ' + from_stmt + qualifier_string,)])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    def test_selection_no_qualifiers(self, create_type, add_remove, from_stmt, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_remove + ' posts ' + from_stmt,)])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('and_bits', list(range(64)))
    def test_qualifier_and_or(self, create_type, add_remove, from_stmt, and_bits, sessioncontroller_impl):
        qualifiers = self.__possible_qualifiers.copy()
        shuffle(qualifiers)

        qualifier_string = ""
        for i in range(6):
            qualifier_string += qualifiers[i] + \
                " and " if (1 << i) & and_bits else " or "

        qualifier_string += qualifiers[-1]

        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new criteria',
                                            UXActionType.CHANGE_MODE,),
                                           ('add posts about "tests"',
                                            UXActionType.NO_OP,),
                                           ('save as "criteria"',
                                            UXActionType.NO_OP,),
                                           ('stop', UXActionType.CHANGE_MODE,
                                            UXActionModeType.MAIN,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_remove + ' posts ' + from_stmt + qualifier_string,)])


@pytest.mark.slow
@pytest.mark.parallel
class TestQualifierVariations:
    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('field_article', ["a", "an", "the"])
    @pytest.mark.parametrize('date_when', ["on", "before", "after"])
    @pytest.mark.parametrize('with_exp', ["with", "without"])
    @pytest.mark.parametrize('comma', [',', ''])
    def test_date_check_variations(self, create_type, with_exp, comma, from_stmt, add_remove, field_article, date_when, sessioncontroller_impl):
        qualifier_string = " {2} {0} post date {1} November 10{3} 2018".format(
            field_article, date_when, with_exp, comma)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('with_exp', ["with", "without"])
    @pytest.mark.parametrize('the', ['the', ''])
    def test_substring_check_variations(self, create_type, with_exp, from_stmt, add_remove, the, sessioncontroller_impl):
        qualifier_string = ' {0} "hello world" in {1} title'.format(
            with_exp, the)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('negate', ["not", ""])
    def test_bool_check_variations(self, create_type, from_stmt, add_remove, negate, sessioncontroller_impl):
        qualifier_string = ' which are {0} verified'.format(negate)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('with_exp', ["with", "without"])
    @pytest.mark.parametrize('compare', ["over", "greater than", "under", "less than", "exactly", "roughly"])
    def test_number_check_variations(self, create_type, from_stmt, add_remove, with_exp, compare, sessioncontroller_impl):
        qualifier_string = ' {0} {1} 10 points'.format(with_exp, compare)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('negate', ["not", ""])
    def test_on_check_variations(self, create_type, from_stmt, add_remove, negate, sessioncontroller_impl):
        qualifier_string = ' {0} on "hello world"'.format(negate)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])

    @pytest.mark.parametrize("create_type,from_stmt,add_remove", [("criteria", "", "add"), ("criteria", "", "remove"), ("selection", "from mock ", "add")])
    @pytest.mark.parametrize('negate', ["not", ""])
    def test_on_check_variations(self, create_type, from_stmt, add_remove, negate, sessioncontroller_impl):
        qualifier_string = ' {0} matching "hello world"'.format(negate)

        add_line = 'add posts ' + from_stmt + qualifier_string
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP,),
                                           ('create a new criteria',),
                                           ('add posts with "hello world" in the title',),
                                           ('save as "hello world"',),
                                           ('stop',),
                                           ('create a new ' + create_type,
                                            UXActionType.CHANGE_MODE,),
                                           (add_line, UXActionType.NO_OP,), ])
