from virtuscale.backend.base import Base
from virtuscale.backend.resource import Resource
from virtuscale.storage_types import StorageType
from virtuscale.decorator.embed_source_decorator import EmbedSourceDecorator

def node(
        name: str, 
        builder: Base, 
        base_image: str, 
        requirements: str,
        storage_type: StorageType,
        model_mount_root: str = "/models",
        ):
    def actual_decorator(func):
        def inner_func(**kwargs):
            builder.add_node(
                EmbedSourceDecorator(target=func),
                base_image=base_image,
                packages=requirements,
                model_mount_root=model_mount_root,
                storage_type=storage_type,
                resource_request=Resource("1"),
                resource_limit=Resource("1"),
            )
        return inner_func
    return actual_decorator

