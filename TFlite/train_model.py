import tensorflow as tf
import tensorflow_hub as tfHub
from utils import readCsv, getData, splitFilenamesAndLabels
from sklearn.preprocessing import MultiLabelBinarizer

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
    
    return dataset, mlb.classes_

trainingDataset, classes = prepareDataset("labels_training.csv")
validationDataset, _ = prepareDataset("labels_validation.csv")

def narrowOutput(output):
    return tf.reshape(tf.reduce_mean(output[0], axis=0), (1,521))
    # return tf.reshape(tf.reduce_max(output[0], axis=0), (1,521))

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
outputNarrowed = tf.reshape(
    tf.reduce_mean(baseModelWrapped.output[0], axis=0),
    (1,521))
output = model(outputNarrowed)
model = tf.keras.Model(baseModelWrapped.input, output)
# model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"],
)

model.fit(
    trainingDataset,
    validation_data=validationDataset,
    epochs=20,
    callbacks=[tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.1,
        patience=5,
        min_lr=0.0001
    )],
    shuffle=True,
    batch_size=16
)

model.save("models/sound_analyzer_v1")
with open("models/sound_analyzer_v1/classes.csv", "w+") as classesFile:
    lines = ["index;label"]

    for index in range(len(classes)):
        lines.append(f"{index};{classes[index]}")

    classesFile.write("\n".join(lines))