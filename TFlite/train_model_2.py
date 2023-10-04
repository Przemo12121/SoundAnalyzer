import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

classes = getClasses("classes.csv")
# xyz = tfHub.load("https://tfhub.dev/google/yamnet/1")
# print(baseModel(np.zeros(16000))[0][0])
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

baseModel = tfHub.KerasLayer(
    "https://tfhub.dev/google/yamnet/1",
    input_shape=(),
    # output_shape=(521, 1024, 64),
    trainable=False)

input = tf.keras.layers.Input(shape=(), name="Input", dtype=tf.float32)
net = baseModel(input)
baseModelWrapped = tf.keras.Model(input, net)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(None,521)),
    # tf.keras.layers.Average(),
    tf.keras.layers.Dense(3, activation="softmax"),
])

# yamnet model outputs shape (input_length/8000,521), required is to average along axis=0 before added layer

# x = tfHub.load("https://tfhub.dev/google/yamnet/1")
# print(x(np.zeros(32000))[0].numpy().mean(axis=0).shape)
# def narrowOutput(output):
#     return output[0]

# outputNarrowed = narrowOutput(baseModel.output)
# output = model(outputNarrowed)
# model = tf.keras.Model(baseModel.input, output)
# model.summary()


# ## OUTPUT LAYER RETURNS WRONG SHAPE

# for f, l in trainingDataset.take(1):
#     print("Shape of features array:", f.numpy().flatten())
#     print("Shape of labels array:", l)

# logits = baseModel(np.zeros(8000))
# print(logits)

# model.compile(
#     optimizer="adam",
#     loss="sparse_categorical_crossentropy",
#     metrics=["accuracy"],
#     run_eagerly=True
# )

# # # print(getData("./data_training/silence/20.wav"))
# # # model.predict(getData("./data_training/silence/20.wav")[0])

# model.fit(
#     trainingDataset,
#     validation_data=validationDataset,
#     epochs=10,
#     shuffle=False
# )

# # # model.save("models/dummy")
# https://stackoverflow.com/questions/59381246/how-to-sequentially-combine-2-tensorflow-models