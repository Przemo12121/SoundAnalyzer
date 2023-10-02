import tensorflow as tf

def getData(path):
    file = tf.io.read_file(path)
    data = tf.audio.decode_wav(file, desired_channels=1)
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

def splitFilenamesAndLabels(csvData):
    filenames = []
    labels = []

    for filename, label in csvData:
        filenames.append(filename)
        labels.append([int(l) for l in label.split(",")])
    
    return (filenames, labels)