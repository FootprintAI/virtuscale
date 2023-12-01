# pylint: disable=no-name-in-module,redefined-outer-name,abstract-method
import tensorflow as tf
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten

from tensorflow.keras import Model
from tensorflow.python.keras.engine.keras_tensor import KerasTensor
from typing import NamedTuple, Dict

from virtuscale.train import node
from virtuscale.compile import compile
from virtuscale.backend.kfp import KfpBuilder
from virtuscale.storage.local_file import LocalFileStorage
from virtuscale.storage_types import StorageType

kfp_builder = KfpBuilder("default")

@node(
    name="foo", 
    builder=kfp_builder, 
    base_image="python3.11",
    requirements="requirements.txt", 
    storage_type=StorageType.LocalFile,
    model_mount_root="/models")
def train(epochs: int) -> Model :
    class MyModel(Model):
        def __init__(self):
            super(MyModel, self).__init__()
            self.conv1 = Conv2D(32, 3, activation="relu")
            self.flatten = Flatten()
            self.d1 = Dense(128, activation="relu")
            self.d2 = Dense(10)

        @tf.function(input_signature=[tf.TensorSpec([None, 28, 28, 1], tf.float32)])
        def call(self, x):
            x = self.conv1(x)
            x = self.flatten(x)
            x = self.d1(x)
            return self.d2(x)

    def do_train():

        mnist = tf.keras.datasets.mnist

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = x_train.reshape(60000, 28, 28, 1).astype("float32") / 255
        x_test = x_test.reshape(10000, 28, 28, 1).astype("float32") / 255

        # Reserve 10,000 samples for validation
        x_val = x_train[-10000:]
        y_val = y_train[-10000:]
        x_train = x_train[:-10000]
        y_train = y_train[:-10000]

        # Create an instance of the model
        model = MyModel()
        model.compile(
            optimizer=tf.keras.optimizers.Adam(),  # Optimizer
            # Loss function to minimize
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            # List of metrics to monitor
            metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
        )
        history = model.fit(
            x_train,
            y_train,
            batch_size=64,
            epochs=epochs,
            # We pass some validation for
            # monitoring validation loss and metrics
            # at the end of each epoch
            validation_data=(x_val, y_val),
        )
        return model

    model = do_train()
    return model

# TODO: add typehint for inference result
def save_model(model):
    pass

# TODO: add typehint for inference result
def infer(model, input_data):
    return model.predict(input_data)

# TODO: define the actual execution order
def run():
    model = train()
    x = tf.random.uniform((1, 28, 28, 1))
    print(infer(model, x))

if __name__ == "__main__":
    train()
    compile(kfp_builder, "mnist_tensorflow_train.yaml")
