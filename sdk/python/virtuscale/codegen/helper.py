import tempfile

from virtuscale.decorator.embed_source_decorator import EmbedSourceDecorator, write_codestr_to_file, import_obj_from_file
from virtuscale.storage_types import StorageType

from typing import NamedTuple, Dict, Callable, Any

def wrap_model_store_closure(esd: EmbedSourceDecorator,
                                        model_name: str,
                                        storage_type: StorageType, 
                                        model_base_path: str,
                                        ) -> Callable:
    closure_code_gen = """
def stub():
    def wrapped_func_with_storage({6}):
        from virtuscale.storage.base import BaseStorage
        from virtuscale.storage.factory import new_storage

        storage_type = {2}
        model_base_path = \"{3}\"
        framework = {4}

        ## add injection callable func ##

{0}
        ## end of injection callable func ##
        model_storage = new_storage(storage_type=storage_type, model_base_path=model_mount_root)
        model_object = {1}({7})
        model_storage.save_model(\"{5}\", model_object, framework)
    return wrapped_func_with_storage
""".format(esd.get_function_source_definition(8),
           esd.get_function_name(),
           storage_type,
           model_base_path,
           esd.inspect_callable_func.get_training_framework_from_signature(),
           model_name,
           ", ".join(esd.inspect_callable_func.get_input_args_with_type()),
           ", ".join(esd.inspect_callable_func.get_input_args()),
           )

    tmpdirname = tempfile.mkdtemp()
    py_file = write_codestr_to_file(tmpdirname, "stub", closure_code_gen)
    stub = import_obj_from_file(py_file, "stub")
    print(py_file)
    print('--codegen--')
    print(closure_code_gen)
    print('--codegen--')
    #exec(closure_code_gen, globals())
    return stub()

