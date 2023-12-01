import inspect

from typing import Callable, get_origin, Any, get_type_hints, List

from virtuscale.framework import Framework

class TypedArgument():
    def __init__(self, t, name: str):
        self.type = t
        self.name = name

class Inspect():
    def __init__(self, func: Callable):
        self._func = func

        self._inputs_outputs: List[TypedArgument] = []

        sig = inspect.signature(self._func)
        sig_type_hints = get_type_hints(self._func)
        for key in sig_type_hints.keys():
            self._inputs_outputs.append(TypedArgument(
                    t = sig_type_hints[key],
                    name = key,
                ))
    def get_input_args_with_type(self) -> List[str]:
        input_args_with_type : List[str] = []
        for input_output in self._inputs_outputs:
            if input_output.name == 'return':
                continue
            input_args_with_type.append('{}: {}'.format(input_output.name,
                                                        input_output.type.__name__))
        return input_args_with_type

    def get_input_args(self) -> List[str]:
        input_args: List[str] = []
        for input_output in self._inputs_outputs:
            if input_output.name == 'return':
                continue
            input_args.append(input_output.name)
        return input_args

    def get_training_framework_from_signature(self):
        from tensorflow import keras
        from tensorflow.keras import Model

        sig = inspect.signature(self._func)
        ret_signature = sig.return_annotation
        if isinstance(Model(), ret_signature):
            return Framework.Tensorflow
        return Framework.Others

    def get_training_framework_from_source(self):
        """ get_training_framework splits the whole source code with newline
        (\n) and lookup each lines with `import xxx`
        """

        func_source = inspect.getsource(self._func)
        for func_source_in_line in func_source.split("\n"):
            if 'import' in func_source_in_line:
                if 'tensorflow' in func_source_in_line:
                    return Framework.Tensorflow
                if 'pytorch' in func_source_in_line:
                    return Framework.Pytorch
        return Framework.Others


def is_parameter(annotation: Any) -> bool:
    if type(annotation) == type:
        return annotation in [str, int, float, bool, dict, list]

    # Annotation could be, for instance `typing.Dict[str, str]`, etc.
    return get_short_type_name(str(annotation)) in ['Dict', 'List']

def get_short_type_name(type_name: str) -> str:
    """Extracts the short form type name.

    This method is used for looking up serializer for a given type.

    For example:
      typing.List -> List
      typing.List[int] -> List
      typing.Dict[str, str] -> Dict
      List -> List
      str -> str

    Args:
      type_name: The original type name.

    Returns:
      The short form type name or the original name if pattern doesn't match.
    """
    match = re.match('(typing\.)?(?P<type>\w+)(?:\[.+\])?', type_name)
    return match['type'] if match else type_name

def is_artifact(annotation: Any) -> bool:
    if type(annotation) == type:
        return type_annotations.is_artifact_class(annotation)
    return False


def is_named_tuple(annotation: Any) -> bool:
    if type(annotation) == type:
        return issubclass(annotation, tuple) and hasattr(
            annotation, '_fields') and hasattr(annotation, '__annotations__')
    return False
