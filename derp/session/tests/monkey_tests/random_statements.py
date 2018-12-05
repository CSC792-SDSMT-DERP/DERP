import random
import pytest

__statements = ['load "mockmodule"', 'unload "mockmodule"' 'read "myselection"', 'stop', 'recall "myselection"',
                'read', 'recall', 'clear', 'clear "myselection"', 'clear "mycriteria"',
                'create a new criteria', 'create a new selection', 'add posts from mock {0}',
                'add posts {0}', 'remove posts {0}', 'save as "myselection"', 'save as "mycriteria"']

__qualifiers = ['with a post date before November 2018', 'which are verified', 'with over 500 points',
                'with "hello world" in the title', 'matching "mycriteria"', 'with the exact title "hello world"']


def __makeQualifier():
    return ' '.join([random.choice(__qualifiers) for _ in range(random.choice(range(0, 5)))])


def __randString():
    s = random.choice(__statements)
    if '{0}' in s:
        s = s.format(__makeQualifier())
    return s


# Generate 1000 random test cases, each with up to 100 statements to test
__test_cases = [[__randString() for _ in range(random.choice(range(1, 100)))]
                for __ in range(1000)]


@pytest.mark.parallel
@pytest.mark.slow
@pytest.mark.monkey
@pytest.mark.parametrize("test_statements", __test_cases)
def test_random_statements(test_statements, sessioncontroller_impl):
    # Throw garbage at the implementation, and make sure it doesn't crash

    try:
        for line in test_statements:
            sessioncontroller_impl.run_input(line)
    except Exception as e:
        print("Failed monkey test case")
        print(test_statements)
        raise
