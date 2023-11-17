import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, splitFilenamesAndLabels
from sklearn.preprocessing import MultiLabelBinarizer
import sys
import time
import json

modelName = sys.argv[1] if len(sys.argv) > 1 else f"model_{time.time()}"
labelsCount = 4

# Prepare training and validation datasets
def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    labels_binary = mlb.transform(labels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels_binary))
    dataset = dataset.map(
        lambda filename, label : (getData(filename), tf.reshape(label, (1,labelsCount))), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset, mlb.classes_

trainingDataset, classes = prepareDataset("data/training/labels.csv")
validationDataset, _ = prepareDataset("data/validation/labels.csv")

# Creates Keras Layer wrapper for tensorflow_hub v1 model
baseModel = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    input_shape=(),
    trainable=True)
input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = baseModel(input)
baseModelWrapped = tf.keras.Model(input, net)

# Creates custom multi-label classification output layers
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(521,)),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(labelsCount, activation="sigmoid"),
])
# Merges model into single model
def narrowOutput(output):
    return tf.reshape(tf.reduce_mean(output[0], axis=0), (1,521))

outputNarrowed = tf.reshape(
    tf.reduce_mean(baseModelWrapped.output[0], axis=0),
    (1,521))
output = model(outputNarrowed)
model = tf.keras.Model(baseModelWrapped.input, output)
model.summary()

# Model compilation and training
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.BinaryCrossentropy(),
    metrics=["accuracy"],
)

history = model.fit(
    trainingDataset,
    validation_data=validationDataset,
    epochs=60,
    callbacks=[tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.1,
        patience=5,
        min_lr=1e-10
    )],
    shuffle=True,
    batch_size=4
)
history.history.pop("lr")

# # Saves tensorflow model and classes
model.save(f"models/{modelName}")
with (
    open(f"models/{modelName}/classes.csv", "w+") as classesFile,
    open(f"output/{modelName}_classes.csv", "w+") as outputClassesFile,
    open(f"models/{modelName}/history.json", "w+") as historyFile
):

    lines = ["index;label"]

    for index in range(len(classes)):
        lines.append(f"{index};{classes[index]}")

    lines = "\n".join(lines)
    json.dump(history.history, historyFile)
    classesFile.write(lines)
    outputClassesFile.write(lines)

# Covnerts to .tflite format
with open(f"output/{modelName}.tflite", "wb") as file:
    file.write(
        tf.lite.TFLiteConverter.from_saved_model(f"./models/{modelName}").convert())