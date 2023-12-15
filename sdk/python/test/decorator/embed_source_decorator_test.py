import tempfile
import unittest

from virtuscale.decorator.embed_source_decorator import EmbedSourceDecorator, import_obj_from_file, get_function_source_definition

class EmbedSourceDecoratorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_embed_source_decorator(self):
        def foo(arg1: int, arg2: int) -> int:
            return arg1 + arg2

        decorated_foo = EmbedSourceDecorator(target=foo)
        assert decorated_foo.get_function_source_definition() == r"""def foo(arg1: int, arg2: int) -> int:
    return arg1 + arg2
"""
        assert decorated_foo.get_function_name() == r"""foo"""

        tmpdirname = tempfile.mkdtemp()
        foo_py_file = decorated_foo.export_to_file(tmpdirname)

        stub = import_obj_from_file(foo_py_file,
                                    decorated_foo.get_function_name())
        assert stub(1,2) == 3
