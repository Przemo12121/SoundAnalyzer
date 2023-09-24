import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import wave
import struct
import csv

def getData(path):
    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = np.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    return waveform

def class_names_from_csv(class_map_csv_text):
  """Returns list of class names corresponding to score vector."""
  class_names = []
  with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      class_names.append(row['display_name'])

  return class_names

model = hub.load('https://tfhub.dev/google/yamnet/1')
class_map_path = model.class_map_path().numpy()
print(class_map_path)
class_names = class_names_from_csv(class_map_path)

for i in range(150, 200):
    data = getData(f"./data/machine_speach/{i+1}.wav")
    scores, embeddings, spectrogram = model(data)
    scores_np = scores.numpy()
    # print(scores)
    # spectrogram_np = spectrogram.numpy()
    infered_class = class_names[scores_np.mean(axis=0).argmax()]
    print(f'./data/silence/{i+1}.wav : sp: {scores[0][2]}, veh: {scores[0][294]}, ra: {scores[0][519]}, rt: {scores[0][322]}')
    print(f'./data/silence/{i+1}.wav : {infered_class}')