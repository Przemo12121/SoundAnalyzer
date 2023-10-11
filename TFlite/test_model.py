import tensorflow as tf
import tensorflow_hub as hub
import wave, struct, numpy

model = tf.saved_model.load("./models/sound_analyzer_v1")
pretrained = hub.load("https://tfhub.dev/google/yamnet/1")

def getData(path):
    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = numpy.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    return waveform

def test(filename):
    result = model(getData(filename))
    print(result)

test("./data_training/silence/18.wav")
test("./data_training/speech/66.wav")
test("./data_training/machine/146.wav")
test("./data_training/machine_speech/163.wav")