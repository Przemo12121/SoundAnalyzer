import tensorflow as tf
import tensorflow_hub as hub
import wave, struct, numpy

# model = tfHub.load("./models/dummy2")
model = tf.saved_model.load("./models/dummy2")
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
    file = tf.io.read_file(filename)
    data, _ = tf.audio.decode_wav(file, desired_channels=1, desired_samples=16000)
    data = tf.squeeze(data, axis=-1)

    o = pretrained(data)

    result = model(tf.reshape(tf.reduce_mean(o[0], axis=0), (1,521)))
    print(result)

test("./data_training/silence/16.wav")
test("./data_training/speech/66.wav")
test("./data_training/machine/146.wav")
test("./data_training/machine_speech/176.wav")