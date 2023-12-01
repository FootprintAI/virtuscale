"""Base Decorator class and utility functions for working with decorators.

There are ways to create decorators that Virtuscale can introspect into.
This is important for documentation generation purposes, so that function
signatures aren't obscured by the (*args, **kwds) signature that decorators
often provide.

1. Derive from Base and implement whatever state you need in your
derived class, and implement the `__call__` method to do your work before
calling into your target. You can retrieve the target via
`super(MyDecoratorClass, self).decorated_target`, and call it with whatever
parameters it needs.

Example:

  class XXXDecorator(Base):
    def __init__(self, target):
      super(XXXDecorator, self).__init__('xxx', target)

    def __call__(self, *args, **kwargs):
      return super(XXXDecorator, self).decorated_target(*args, **kwargs)

  def xxx_calls(target):
    return XXXDecorator(target)
"""
import inspect
from typing import Dict, Any


def _make_default_values(fullargspec: inspect.FullArgSpec) -> Dict[str, Any]:
  """Returns default values from the function's fullargspec."""
  if fullargspec.defaults is not None:
    defaults = {
        name: value for name, value in zip(
            fullargspec.args[-len(fullargspec.defaults):], fullargspec.defaults)
    }
  else:
    defaults = {}

  if fullargspec.kwonlydefaults is not None:
    defaults.update(fullargspec.kwonlydefaults)

  return defaults


def fullargspec_to_signature(
    fullargspec: inspect.FullArgSpec) -> inspect.Signature:
  """Repackages fullargspec information into an equivalent inspect.Signature."""
  defaults = _make_default_values(fullargspec)
  parameters = []

  for arg in fullargspec.args:
    parameters.append(
        inspect.Parameter(
            arg,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=defaults.get(arg, inspect.Parameter.empty),
        )
    )

  if fullargspec.varargs is not None:
    parameters.append(
        inspect.Parameter(fullargspec.varargs, inspect.Parameter.VAR_POSITIONAL)
    )

  for kwarg in fullargspec.kwonlyargs:
    parameters.append(
        inspect.Parameter(
            kwarg,
            inspect.Parameter.KEYWORD_ONLY,
            default=defaults.get(kwarg, inspect.Parameter.empty),
        )
    )

  if fullargspec.varkw is not None:
    parameters.append(
        inspect.Parameter(fullargspec.varkw, inspect.Parameter.VAR_KEYWORD)
    )

  return inspect.Signature(parameters)

class Base(object):
  """Base class for decorators.

  Base captures and exposes the wrapped target, and provides details
  about the current decorator.
  """

  def __init__(self,
               decorator_name,
               target,
               decorator_doc='',
               decorator_argspec=None):
    self._decorated_target = target
    self._decorator_name = decorator_name
    self._decorator_doc = decorator_doc
    self._decorator_argspec = decorator_argspec
    if hasattr(target, '__name__'):
      self.__name__ = target.__name__
    if hasattr(target, '__qualname__'):
      self.__qualname__ = target.__qualname__
    if self._decorator_doc:
      self.__doc__ = self._decorator_doc
    elif hasattr(target, '__doc__') and target.__doc__:
      self.__doc__ = target.__doc__
    else:
      self.__doc__ = ''

    if decorator_argspec:
      self.__signature__ = fullargspec_to_signature(decorator_argspec)
    elif callable(target):
      try:
        self.__signature__ = inspect.signature(target)
      except (TypeError, ValueError):
        # Certain callables such as builtins can not be inspected for signature.
        pass

  def __get__(self, instance, owner):
    return self._decorated_target.__get__(instance, owner)

  def __call__(self, *args, **kwargs):
    return self._decorated_target(*args, **kwargs)

  @property
  def decorated_target(self):
    return self._decorated_target

  @decorated_target.setter
  def decorated_target(self, decorated_target):
    self._decorated_target = decorated_target

  @property
  def decorator_name(self):
    return self._decorator_name

  @property
  def decorator_doc(self):
    return self._decorator_doc

  @property
  def decorator_argspec(self):
    return self._decorator_argspec
