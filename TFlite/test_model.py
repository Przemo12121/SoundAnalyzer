# import tensorflow_hub as tfHub
import tensorflow as tf
import wave, struct, numpy

# model = tfHub.load("./models/dummy2")
model = tf.saved_model.load("./models/dummy2")

def getData(path):
    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = numpy.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    return waveform

# data = getData()
# print(data)
print(model)

# file = tf.io.read_file(path)
    # print(file)
data = getData("./data_training/silence/16.wav")
# print(data)
# tf.audio.encode_wav([data, 1], 16000, "./test.wav")

# data, _ = tf.audio.decode_wav("./data_training/speech/72.wav", desired_channels=1)
# print(data)
result = model(data)
print(result)