import tensorflow as tf
import tensorflow_hub as hub
import wave, struct, numpy


pathToModel = "./models/sv11"
model = tf.saved_model.load(pathToModel)
import json


labels = ["clapping", "machine", "silence", "speech", "whistling"]
durations = list(range(5, 26, 5))
treshold = 0.5

succ = "successes"
occ = "occurences"
fp = "falsePositives"
miss = "misstakes"

x = lambda : { a:0 for a in [occ, fp, succ, miss] }
y = lambda : { l:x() for l in labels }

results = { d:y() for d in durations }

def getData(path):
    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = numpy.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    duration = len(waveform) / wave_data.getframerate()

    return waveform, round(duration)

def analyze(output, duration, targets):
    global results
    global treshold

    for t in targets:
        results[duration][t][occ] += 1

    for index, p in output:
        label = labels[index]
        isTarget = label in targets

        if p >= treshold and isTarget:
            results[duration][label][succ] += 1
        elif p >= treshold and not isTarget:
            results[duration][label][fp] += 1
        elif p < treshold and isTarget:
            results[duration][label][miss] += 1

def test(ds):
    global results

    for set in ds:
        path = set[0]
        targets = set[1]
        
        data, _ = getData(path)
        duration = 10

        output = enumerate(model(data).numpy()[0])
        analyze(output, duration, targets)  

test([
    ["w_short.wav", ["whistling", "silence"]],
    ["speech_silence.wav", ["speech", "silence"]],
    ["m_s_short.wav", ["speech", "machine"]],
])

# for d in durations:
#     dataset = 

# print(results)
with open("testResults.json", "w+") as file:
    json.dump(results, file)