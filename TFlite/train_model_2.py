import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

classes = getClasses("classes.csv")

premodel = tfHub.load("https://tfhub.dev/google/yamnet/1")

def x(filename, label):
    data = getData(filename)
    predictions = premodel(data)
    return tf.reshape(tf.reduce_mean(predictions[0], axis=0), (1,521)), tf.reshape(label, (1,3))
    
    # print(label)
    # return getData(filename), tf.reshape(label, (1,3))
    # return getData(filename), label

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    labels_binary = mlb.transform(labels)

    print(mlb.classes_)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels_binary))
    dataset = dataset.map(
        x,
        # lambda filename, label : (getData(filename), tf.reshape(label, (1,3))), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

def narrowOutput(output):
    return tf.reduce_mean(output[0], axis=0)

def averageOutput(output):
    return tf.reduce_mean(output, axis=0)
    # return tf.reduce_max(output, axis=0)

# baseModel = tfHub.KerasLayer(
#     "https://tfhub.dev/google/yamnet/1",
#     input_shape=(),
#     trainable=False)
# input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
# net = baseModel(input)
# baseModelWrapped = tf.keras.Model(input, net)

model = tf.keras.Sequential([
    # tf.keras.layers.Lambda(lambda x : tf.reduce_mean(x, axis=0)),
    tf.keras.layers.Input(shape=(521,)),
    # tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax"),
])
# outputNarrowed = narrowOutput(baseModelWrapped.output)
# output = model(outputNarrowed)
# model = tf.keras.Model(baseModelWrapped.input, output)
model.summary()

# outputAveraged = averageOutput(model.output)
# output = model(outputAveraged)
# model = tf.keras.Model(model.input, output)

lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=5,
    min_lr=0.0001
)

# lrs = tf.keras.optimizers.schedules.ExponentialDecay(
#     initial_learning_rate=0.00001,
#     decay_steps=10000,
#     decay_rate=0.96
# )

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"],
    run_eagerly=True
)

model.fit(
    trainingDataset,
    # validation_split=0.2,
    validation_data=validationDataset,
    epochs=10,
    callbacks=[lr]
    # shuffle=True,
    # batch_size=4
)
# model.save("models/dummy2")