import abc

from typing import Callable
from virtuscale.framework import Framework

class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def save_model(framework: Framework, model_name: str, model_object: dict) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def load_model(framework: Framework, model_path: str)-> dict:
        raise NotImplementedError()
