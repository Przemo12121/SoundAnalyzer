import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

classes = getClasses("classes.csv")

def x(filename, label):
    print(label)
    return getData(filename), label

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    labels_binary = mlb.transform(labels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels_binary))
    dataset = dataset.map(
        lambda filename, label : (getData(filename), label), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

feature_extractor_layer = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    trainable=False)
input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = feature_extractor_layer(input)
# output = tf.keras.layers.concatenate([net[0], net[1], net[2]])
output = tf.keras.layers.Dense(4, activation="softmax")(net[0])
model = tf.keras.Model(input, output)

## OUTPUT LAYER RETURNS WRONG SHAPE

# model.summary()
for f, l in trainingDataset.take(1):
    print("Shape of features array:", f.numpy().flatten())
    print("Shape of labels array:", l)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=True
)

# # print(getData("./data_training/silence/20.wav"))
# # model.predict(getData("./data_training/silence/20.wav")[0])

model.fit(
    trainingDataset,
    validation_data=validationDataset,
    epochs=10,
    shuffle=False
)

# # model.save("models/dummy")