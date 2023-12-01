import abc

from virtuscale.backend.resource import Resource
from virtuscale.storage_types import StorageType

from typing import Any, Callable, Mapping, Sequence

class Base(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_node(
        self, 
        func, 
        base_image: str, 
        packages: str, 
        storage_type: StorageType,
        model_mount_root: str,
        args:tuple, 
        kwargs:dict,
        resource_request: Resource = Resource("1"), 
        resource_limit: Resource = Resource("1"), 
        ):
        """ Return new node """
        return NotImplemented

    @abc.abstractmethod
    def add_volume(self, size: str = '1Gi'):
        """ Return compile the graph"""
        return NotImplemented

    @abc.abstractmethod
    def compile(self):
        return NotImplemented
