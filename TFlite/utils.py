import tensorflow as tf

def getData(path):
    file = tf.io.read_file(path)
    data, _ = tf.audio.decode_wav(file, desired_channels=1, desired_samples=16000)
    data = tf.squeeze(data, axis=-1)
    return data

def readCsv(path: str, delimiter: str):
    rows = []

    with open(path, "r") as file:
        lines = file.readlines()
        lines.pop(0)

        for row in lines:
            rows.append(row.strip().split(delimiter))

    return rows

def splitFilenamesAndLabels(csvData):
    filenames = []
    labels = []

    for filename, label in csvData:
        filenames.append(filename)
        labels.append(label.split(","))
    
    return (filenames, labels)