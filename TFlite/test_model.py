import tensorflow as tf
import tensorflow_hub as hub
import wave, struct, numpy


pathToModel = "./models/sv10"
model = tf.saved_model.load(pathToModel)
# pretrained = hub.load("https://tfhub.dev/google/yamnet/1")

def getData(path):
    print("")
    print(path)
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

test("./data/training/silence/18.wav")
test("./data/training/speech/66.wav")
test("./data/training/machine/146.wav")
test("./data/training/machine_speech/163.wav")
test("./data/training/whistling/276.wav")
test("./data/training/machine_whistling/325.wav")
test("./data/training/clapping/446.wav")
test("./data/training/machine_clapping/514.wav")
test("s_short.wav")
test("m_s_short.wav")
test("c_short.wav")
test("m_c_short.wav")
test("w_short.wav")
test("m_w_short.wav")