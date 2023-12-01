import unittest
import inspect

from virtuscale.runtime import make_func

def foo() -> int:
    print("hello foo")
    return 5

def bar(int1:int, str2: int):
    print("hello bar")

class RuntimeTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_copy_function(self):
        """ in this test, we want to create a dynamic function,
        whose signature is matched with `bar`
        but its implementation is `foo`
        """

        expected_params = inspect.signature(bar).parameters.values()
        made_bar_func = make_func(expected_params, foo)
        assert made_bar_func(1,2) == 5
