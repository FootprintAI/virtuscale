import unittest

from typing import NamedTuple, Dict, Callable
from tensorflow.keras import Model
from virtuscale.inspect import Inspect
from virtuscale.inspect import Framework

class mockTensorflowModel(Model):
    def __init__(self):
        pass
    def call(self, inputs):
        pass

def mockTensorflowModekMakerFunc(foo: str, bar: int) -> Model:
    try:
        import tensorflow as tf
    except ImportError:
        pass
    return mockTensorflowModel()

class InspectTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_function_signature(self):
        ins = Inspect(func=mockTensorflowModekMakerFunc)
        assert ins.get_training_framework_from_signature() == Framework.Tensorflow
        assert ins.get_training_framework_from_source() == Framework.Tensorflow
        assert ', '.join(ins.get_input_args_with_type()) == 'foo: str, bar: int'

