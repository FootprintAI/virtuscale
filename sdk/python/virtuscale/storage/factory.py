
from virtuscale.storage_types import StorageType
from virtuscale.storage.base import BaseStorage
from virtuscale.storage.local_file import LocalFileStorage

def new_storage(storage_type: StorageType, *args, **kwargs) -> BaseStorage:
    if storage_type == StorageType.LocalFile:
        return LocalFileStorage(*args, **kwargs)
    raise NotImplementedError()

