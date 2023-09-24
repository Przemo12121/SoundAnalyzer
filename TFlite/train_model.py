import tensorflow as tf
# import tensorflow_hub as hub
import numpy as np
import wave
import struct
import os

def getData(path):
    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = np.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    return waveform



def getClassesWithIds(path: str, delimiter: str):
  classes = {}

  with open(path, "r") as file:
    lines = file.readlines()
    lines.pop(0)

    for row in lines:
      keys = row.strip().split(delimiter)
      classes[keys[1]] = keys[0]

  return classes

classesWithIds = getClassesWithIds("classes_custom.csv", ";")
classes = list(classesWithIds.keys())
print(classesWithIds)
print(classes)

x = os.listdir("./data_test")
for i in x:
   print(i)
print(len(x))
# ds = tf.data.Dataset.from_input_slices
#https://www.tensorflow.org/guide/data

# print(ds.class_names)