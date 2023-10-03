import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np

classes = getClasses("classes.csv")

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    dataset = dataset.map(
        lambda filename, label : (getData(filename), label), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

feature_extractor_layer = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    trainable=True)
input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = feature_extractor_layer(input)
# output = tf.keras.layers.concatenate([net[0], net[1], net[2]])
output = tf.keras.layers.Dense(3, activation="softmax")(net[0])
model = tf.keras.Model(input, output)

model.summary()
print(model.input_spec)
# print(output)

for f, l in validationDataset.take(1):
    print("Shape of features array:", f.numpy().flatten())
    print("Shape of labels array:", l.shape)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# print(getData("./data_training/silence/20.wav"))
# model.predict(getData("./data_training/silence/20.wav")[0])

model.fit(
    trainingDataset,
    validation_data=validationDataset,
    epochs=10
)

# # model.save("models/dummy")