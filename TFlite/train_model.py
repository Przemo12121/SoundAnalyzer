import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

classes = getClasses("classes.csv")

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    labels_binary = mlb.transform(labels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels_binary))
    dataset = dataset.map(
        lambda filename, label : (getData(filename), tf.reshape(label, (1,3))), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

def narrowOutput(output):
    return output[0]

def averageOutput(output):
    return tf.reduce_mean(output, axis=0)
    # return tf.reduce_max(output, axis=0)

baseModel = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    input_shape=(),
    trainable=False)
input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = baseModel(input)
baseModelWrapped = tf.keras.Model(input, net)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(521,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax"),
])
outputNarrowed = narrowOutput(baseModelWrapped.output)
output = model(outputNarrowed)
model = tf.keras.Model(baseModelWrapped.input, output)
model.summary()

outputAveraged = averageOutput(model.output)
output = model(outputAveraged)
model = tf.keras.Model(model.input, output)

model.compile(
    optimizer=tf.keras.optimizers.SGD(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"],
    # run_eagerly=True
)

model.fit(
    trainingDataset,
    validation_data=validationDataset,
    epochs=20,
    shuffle=True,
    # batch_size=4
)
model.save("models/dummy2")