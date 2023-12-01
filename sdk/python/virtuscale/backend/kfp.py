import inspect
import time

from kfp import dsl, compiler
from kfp.components import create_component_from_func
from virtuscale.backend.base import Base
from virtuscale.backend.resource import Resource
from virtuscale.exception import BadParamException
from virtuscale.storage_types import StorageType
from virtuscale.storage.base import BaseStorage
from virtuscale.storage.factory import new_storage
from virtuscale.decorator.embed_source_decorator import EmbedSourceDecorator
from virtuscale.codegen.helper import wrap_model_store_closure
from virtuscale.runtime import make_func

from typing import Any, Callable, Mapping, Sequence

class NodeSpec():
    def __init__(self, 
                 name: str,
                 func: EmbedSourceDecorator,
                 base_image: str,
                 packages: str,
                 storage_type: StorageType,
                 model_mount_root: str,
                 resource_request: Resource,
                 resource_limit: Resource,
                 is_entry: bool = False,
                 ):
        self.name = name
        self.is_entry = is_entry,
        self.func = func
        self.base_image = base_image
        self.packages = packages
        self.storage_type = storage_type
        self.model_mount_root = model_mount_root
        self.resource_request = resource_request
        self.resource_limit = resource_limit

    def create_container_op(self) -> dsl.ContainerOp:
        print("ontainer op, storage_type:{}".format(self.storage_type))
        wrapped_func = wrap_func_with_storage(
            model_name = self.name,
            actual_func = self.func,
            storage_type = self.storage_type,
            model_base_path = self.model_mount_root,
        )
        op_factory = create_component_from_func(
            func = wrapped_func,
            base_image = self.base_image,
        )
        # create a local var dict for storing all required local vairalbes
        # for the self.func
        kwargs = {}
        for param in inspect.signature(self.func).parameters.values():
            kwargs[param.name] = '_global_{}'.format(param.name)

        container_op = op_factory(**kwargs)
        return container_op.set_cpu_request(
                self.resource_request.cpu
            ).set_cpu_limit(self.resource_limit.cpu) 

def wrap_func_with_storage(model_name: str, 
                           actual_func: EmbedSourceDecorator, 
                           storage_type: StorageType,
                           model_base_path: str)-> Callable:
    closure = wrap_model_store_closure(
            actual_func,
            model_name,
            storage_type,
            model_base_path)
    return closure

class KfpBuilder(Base):

    def __init__(self, name: str):
        print("__kfp_backend is initialized")
        self.name = name

        self._op_node_factory_dict: dict[str: NodeSpec] = {}

    def get_entry_node(self) -> NodeSpec:
        # FIXME: ensure only one NodeSpec is entry
        for name in self._op_node_factory_dict.keys():
            if self._op_node_factory_dict[name].is_entry:
                return self._op_node_factory_dict[name]

    def add_node(self,
            func, 
            base_image: str,
            packages: str, 
            model_mount_root: str = "/models",
            storage_type: StorageType = StorageType.LocalFile,
            resource_request: Resource = Resource("1"), 
            resource_limit: Resource = Resource("1"),
            ):

        self._op_node_factory_dict[func.__name__] = NodeSpec(
            name = func.__name__, 
            func = func,
            base_image = base_image, 
            packages = packages,
            model_mount_root = model_mount_root,
            storage_type = storage_type,
            resource_request = resource_request,
            resource_limit = resource_limit,
        )

    def add_volume(self, size: str = '1Gi'):
        pvc_name = 'my-awesome-kf-workshop-%d'% int(time.time())
        vop = dsl.VolumeOp(
            name="{}-volume".format(self.name),
            resource_name=pvc_name,
            size=size,
            modes=dsl.VOLUME_MODE_RWO,
            generate_unique_name=False,
            # do not use unique name, so we could statically bind the pvc name to tensorboard
            # otherwise, the tensorboard are unlikely to automatically retrieve the pvc name as it is generated during runtime
        )
        return vop
    def compile(self, output_file: str):
        pipeline_decorator = dsl.pipeline(name='virtuscalepipeline', description='A virtuscale pipeline')
        compiler.Compiler(mode=dsl.PipelineExecutionMode.V1_LEGACY).compile(
            pipeline_decorator(pipeline_entry(self)), output_file)

def pipeline_entry(builder: KfpBuilder):
    def entry():

        # assume that we only have one volume per build
        #if len(__kfp_backend._op_volume_dict) == 0:
        #    raise BadParamException("number of op_volume can not be more than oce")
        if len(builder._op_node_factory_dict) == 0:
            raise BadParamException("number of no_node can not be more than once")

        vop = builder.add_volume()
        for key in builder._op_node_factory_dict.keys():
            node_spec = builder._op_node_factory_dict[key]
            container_op = node_spec.create_container_op()
            container_op.add_pvolumes({
                node_spec.model_mount_root:vop.volume,
            })
    return entry

    # create a function wrapper with entry node's signature
    # and $entry function's implementation
    entry_node = builder.get_entry_node()
    entry_params = inspect.signature(entry_node.func).parameters.values()
    return make_func(entry_params, entry)
