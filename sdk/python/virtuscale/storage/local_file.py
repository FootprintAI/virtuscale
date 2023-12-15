from typing import Callable

from virtuscale.storage.base import BaseStorage
from virtuscale.framework import Framework

class LocalFileStorage(BaseStorage):
    def __init__(self, model_base_path: str):
        self.model_base_path = model_base_path

    def save_model(framework: Framework, model_name: str, model_object: dict) -> str:
        if framework == Framework.Tensorflow:
            import tensorflow as tf
            model_save_path = os.path.join(self.model_base_path, model_name, '1')
            tf.saved_model.save(model_object, model_save_path)
            return model_save_path
        raise NotImplementedError()

    def load_model(framework: Framework, model_name: str) -> dict:
        if framework == Framework.Tensorflow:
            import tensorflow as tf
            model_load_path = os.path.join(self.model_base_path, model_name)
            return tf.saved_model.load(model_load_path)
        raise NotImplementedError()
