import inspect
import itertools
import os
import textwrap

from typing import NamedTuple, Dict, Callable, Any
from virtuscale.decorator.base import Base
from virtuscale.inspect import Inspect

class EmbedSourceDecorator(Base):
    def __init__(
            self, 
            target: Callable,
            decorator_name=None,
            decorator_doc='',
            decorator_argspec=None):
        if not decorator_name:
            decorator_name = target.__name__ # use function default name

        self.callable_func = target
        self.func_name = decorator_name
        self.inspect_callable_func = Inspect(target)
        super(EmbedSourceDecorator, self).__init__(
                decorator_name=decorator_name,
                target=target,
                decorator_doc=decorator_doc,
                decorator_argspec=decorator_argspec,
                )

    def export_to_file(self, python_dir: str) -> str:
        return write_codestr_to_file(
                python_dir, 
                self.get_function_name(), 
                get_function_source_definition(self.callable_func))

    def get_function_source_definition(self, indent: int = 0) -> str:
        return get_function_source_definition(self.callable_func, indent)

    def get_function_name(self) -> str:
        return self.func_name

    def func(self) -> Callable:
        return self.callable_func

    def __call__(self, *args, **kwargs):
        return super(EmbedSourceDecorator, self).decorated_target(*args, **kwargs)

def get_function_source_definition(callable_func: Callable, indent_num:int = 0) -> str:
    func_code = inspect.getsource(callable_func)

    # Function might be defined in some indented scope (e.g. in another
    # function). We need to handle this and properly dedent the function source
    # code
    func_code = textwrap.dedent(func_code)
    func_code_lines = func_code.split('\n')

    # Removing possible decorators (can be multiline) until the function
    # definition is found
    func_code_lines = itertools.dropwhile(lambda x: not x.startswith('def'),
                                          func_code_lines)

    if not func_code_lines:
        raise ValueError(
            f'Failed to dedent and clean up the source of function "{func.__name__}". It is probably not properly indented.'
        )

    return indent('\n'.join(func_code_lines), indent_num)

def indent(text, amount, ch=' '):
    return textwrap.indent(text, amount * ch)

def import_obj_from_file(python_path: str, obj_name: str) -> Any:
    import sys

    sys.path.insert(0, os.path.dirname(python_path))
    module_name = os.path.splitext(os.path.split(python_path)[1])[0]
    module = __import__(module_name, fromlist=[obj_name])
    if not hasattr(module, obj_name):
        raise ValueError(
            f'Object "{obj_name}" not found in module {python_path}.')
    return getattr(module, obj_name)

def write_codestr_to_file(python_dir: str, module_name: str, py_source: str) -> str:
    py_file = os.path.join(python_dir, '{}.py'.format(module_name))
    with open(py_file, 'w') as w:
        w.write(py_source)
    return py_file

