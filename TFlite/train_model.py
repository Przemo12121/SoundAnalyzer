import tensorflow as tf
from utils import readCsv, getData, getClasses, splitFilenamesAndLabels

classes = getClasses("classes.csv")

def prepareDataset(pathToLabels: str):
    filenamesWithLabels = readCsv(pathToLabels, ";")
    filenames, labels = splitFilenamesAndLabels(filenamesWithLabels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    dataset = dataset.map(
        lambda filename, label: (getData(filename), label), 
        num_parallel_calls=tf.data.AUTOTUNE)
    
    return dataset

trainingDataset = prepareDataset("labels_training.csv")
validationDataset = prepareDataset("labels_validation.csv")

for f, l in trainingDataset.take(1):
    print("Shape of features array:", f)
    print("Shape of labels array:", l)



# ds = tf.data.Dataset.from_input_slices
#https://www.tensorflow.org/guide/data
#https://github.com/ashrefm/multi-label-soft-f1/blob/master/Multi-Label%20Image%20Classification%20in%20TensorFlow%202.0.ipynb