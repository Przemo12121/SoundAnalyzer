import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

classes = getClasses("classes.csv")
xyz = tfHub.load("https://tfhub.dev/google/yamnet/1")
def x(waveData, label):
    scores, _, _ = xyz(np.zeros(16000))
    mean = tf.reduce_mean(scores, axis=0)
    return tf.transpose(mean), label

def wavedata(filename, label):
    return getData(filename), tf.reshape(label, (1,3))

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    labels_binary = mlb.transform(labels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels_binary))
    dataset = dataset.map(wavedata)
    # dataset = dataset.map(x)
    # dataset = dataset.map(
    #     lambda filename, label : (getData(filename), label), 
    #     num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

def narrowOutput(output):
    scores = output[0]
    return scores
def averageOutput(output):
    return tf.reduce_mean(output, axis=0)

baseModel = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    input_shape=(),
    trainable=False)
input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = baseModel(input)
baseModelWrapped = tf.keras.Model(input, net)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(521,)),
    tf.keras.layers.Dense(3, activation="softmax"),
])
outputNarrowed = narrowOutput(baseModelWrapped.output)
output = model(outputNarrowed)
model = tf.keras.Model(baseModelWrapped.input, output)
model.summary()

# model.compile(
#     optimizer="adam",
#     loss="categorical_crossentropy",
#     metrics=["accuracy"],
#     run_eagerly=True
# )

# model.fit(
#     trainingDataset,
#     validation_data=validationDataset,
#     epochs=10,
#     shuffle=False
# )

# x = tf.constant([10, 20, 30, 5, 10, 15], shape=(2,3))
# print(x)
# print(tf.reduce_mean(x, axis=0))
# # # model.save("models/dummy")
# https://stackoverflow.com/questions/59381246/how-to-sequentially-combine-2-tensorflow-models