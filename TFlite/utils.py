import tensorflow as tf
import tensorflow_io as tfio

def getData(path):
    # print(tf.strings.as_string(path).numpy())
    file = tf.io.read_file(path)
    # print(file)
    data, _ = tf.audio.decode_wav(file, desired_channels=1)

    return data

def getClasses(path: str):
    classesIdMapping = {}
    csv = readCsv(path, ";")

    for pair in csv:
        classesIdMapping[pair[0]] = pair[1]

    return [classesIdMapping[i] for i in sorted(classesIdMapping)]

def readCsv(path: str, delimiter: str):
    rows = []

    with open(path, "r") as file:
        lines = file.readlines()
        lines.pop(0)

        for row in lines:
            rows.append(row.strip().split(delimiter))

    return rows

xyz = ['silence', 'speech', 'machine']

def splitFilenamesAndLabels(csvData):
    filenames = []
    labels = []

    for filename, label in csvData:
        filenames.append(filename)
        # labels.append([float(l) for l in label.split(",")])
        labels.append(label.split(",")) #tm2
    
    return (filenames, labels)