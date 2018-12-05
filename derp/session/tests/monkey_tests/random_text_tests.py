import random
import pytest


def __randString():
    return "".join([chr(random.choice(range(0, 255))) for _ in range(random.choice(range(0, 100)))])


# Generate 1000 random test cases, each with up to 100 statements to test
__test_cases = [[__randString() for _ in range(random.choice(range(1, 100)))]
                for __ in range(1000)]


@pytest.mark.parallel
@pytest.mark.slow
@pytest.mark.monkey
@pytest.mark.parametrize("test_statements", __test_cases)
def test_random_keywords(test_statements, sessioncontroller_impl):
    # Throw garbage at the implementation, and make sure it doesn't crash

    try:
        for line in test_statements:
            sessioncontroller_impl.run_input(line)
    except Exception as e:
        print("Failed monkey test case")
        print(test_statements)
        raise
