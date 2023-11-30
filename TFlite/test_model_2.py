import tensorflow as tf
import tensorflow_hub as hub
import wave, struct, numpy


pathToModel = "./models/sound_analyzer_v2"
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

# def analyze(output, duration, targets):
#     global results
#     global treshold

#     for t in targets:
#         results[duration][t][occ] += 1

#     for index, p in output:
#         label = labels[index]
#         isTarget = label in targets

#         if p >= treshold and isTarget:
#             results[duration][label][succ] += 1
#         elif p >= treshold and not isTarget:
#             results[duration][label][fp] += 1
#         elif p < treshold and isTarget:
#             results[duration][label][miss] += 1

def test(ds):
    global results
    global treshold

    for set in ds:
        path = set[0]
        targets = set[1]
        
        data, duration = getData(path)
        # duration = 10

        output = enumerate(model(data).numpy()[0])
        # analyze(output, duration, targets)
        for t in targets:
            results[duration][t][occ] += 1

        for index, p in output:
            label = labels[index]
            isTarget = label in targets

            if p >= treshold and isTarget:
                results[duration][label][succ] += 1
            elif p >= treshold and not isTarget:
                print(path, " ", label, " ", targets, " ", duration)
                results[duration][label][fp] += 1
            elif p < treshold and isTarget:
                results[duration][label][miss] += 1

test([
    ["testDs/5_sil_sp.wav", ["speech", "silence"]],
    ["testDs/10_sil_sp.wav", ["speech", "silence"]],
    ["testDs/15_sil_sp.wav", ["speech", "silence"]],
    ["testDs/20_sil_sp.wav", ["speech", "silence"]],
    ["testDs/25_sil_sp.wav", ["speech", "silence"]],
    ["testDs/5_sil_sp2.wav", ["speech", "silence"]],
    ["testDs/10_sil_sp2.wav", ["speech", "silence"]],
    ["testDs/15_sil_sp2.wav", ["speech", "silence"]],
    ["testDs/20_sil_sp2.wav", ["speech", "silence"]],
    ["testDs/25_sil_sp2.wav", ["speech", "silence"]],
    ["testDs/5_sil_sp3.wav", ["speech", "silence"]],
    ["testDs/10_sil_sp3.wav", ["speech", "silence"]],
    ["testDs/15_sil_sp3.wav", ["speech", "silence"]],
    ["testDs/20_sil_sp3.wav", ["speech", "silence"]],
    ["testDs/25_sil_sp3.wav", ["speech", "silence"]],
    ["testDs/5_sp.wav", ["speech"]],
    ["testDs/10_sp.wav", ["speech"]],
    ["testDs/15_sp.wav", ["speech"]],
    ["testDs/20_sp.wav", ["speech"]],
    ["testDs/25_sp.wav", ["speech"]],
    ["testDs/25_sp.wav", ["speech"]],
    ["testDs/5_sil_wh.wav", ["whistling", "silence"]],
    ["testDs/10_sil_wh.wav", ["whistling", "silence"]],
    ["testDs/15_sil_wh.wav", ["whistling", "silence"]],
    ["testDs/20_sil_wh.wav", ["whistling", "silence"]],
    ["testDs/25_sil_wh.wav", ["whistling", "silence"]],
    ["testDs/5_wh.wav", ["whistling"]], 
    ["testDs/10_wh.wav", ["whistling"]],
    ["testDs/15_wh.wav", ["whistling"]],
    ["testDs/20_wh.wav", ["whistling"]],
    ["testDs/25_wh.wav", ["silence", "whistling"]],
    ["testDs/5_sil_wh2.wav", ["whistling", "silence"]],
    ["testDs/10_sil_wh2.wav", ["whistling", "silence"]],
    ["testDs/15_sil_wh2.wav", ["whistling", "silence"]],
    ["testDs/20_sil_wh2.wav", ["whistling", "silence"]],
    ["testDs/25_sil_wh2.wav", ["whistling", "silence"]],
    ["testDs/5_sil_cp.wav", ["clapping", "silence"]],
    ["testDs/10_sil_cp.wav", ["clapping", "silence"]],
    ["testDs/15_sil_cp.wav", ["clapping", "silence"]],
    ["testDs/20_sil_cp.wav", ["clapping", "silence"]],
    ["testDs/25_sil_cp.wav", ["clapping", "silence"]],
    ["testDs/5_sil_cp2.wav", ["clapping", "silence"]],
    ["testDs/10_sil_cp2.wav", ["clapping", "silence"]],
    ["testDs/15_sil_cp2.wav", ["clapping", "silence"]],
    ["testDs/20_sil_cp2.wav", ["clapping", "silence"]],
    ["testDs/25_sil_cp2.wav", ["clapping", "silence"]],
    ["testDs/5_sil_cp3.wav", ["clapping", "silence"]],
    ["testDs/10_sil_cp3.wav", ["clapping", "silence"]],
    ["testDs/15_sil_cp3.wav", ["clapping", "silence"]],
    ["testDs/20_sil_cp3.wav", ["clapping", "silence"]],
    ["testDs/25_sil_cp3.wav", ["clapping", "silence"]],
    ["testDs/5_mch_sp.wav", ["speech", "machine"]],
    ["testDs/10_mch_sp.wav", ["speech", "machine"]],
    ["testDs/15_mch_sp.wav", ["speech", "machine"]],
    ["testDs/20_mch_sp.wav", ["speech", "machine"]],
    ["testDs/25_mch_sp.wav", ["speech", "machine"]],
    ["testDs/5_mch_cp.wav", ["clapping", "machine"]],
    ["testDs/10_mch_cp.wav", ["clapping", "machine"]],
    ["testDs/15_mch_cp.wav", ["clapping", "machine"]],
    ["testDs/20_mch_cp.wav", ["clapping", "machine"]],
    ["testDs/25_mch_cp.wav", ["clapping", "machine"]],
    ["testDs/5_mch_wh.wav", ["whistling", "machine"]],
    ["testDs/10_mch_wh.wav", ["whistling", "machine"]],
    ["testDs/15_mch_wh.wav", ["whistling", "machine"]],
    ["testDs/20_mch_wh.wav", ["whistling", "machine"]],
    ["testDs/25_mch_wh.wav", ["whistling", "machine"]],
    ["testDs/5_sil_sp_cp_wh.wav", ["silence", "speech",  "whistling", "clapping"]],
    ["testDs/10_sil_sp_cp_wh.wav", ["silence", "speech",  "whistling", "clapping"]],
    ["testDs/15_sil_sp_cp_wh.wav", ["silence", "speech",  "whistling", "clapping"]],
    ["testDs/20_sil_sp_cp_wh.wav", ["silence", "speech",  "whistling", "clapping"]],
    ["testDs/25_sil_sp_cp_wh.wav", ["silence", "speech",  "whistling", "clapping"]],
    ["testDs/5_mch_sp_cp_wh.wav", ["machine", "speech",  "whistling", "clapping"]],
    ["testDs/10_mch_sp_cp_wh.wav", ["machine", "speech",  "whistling", "clapping"]],
    ["testDs/15_mch_sp_cp_wh.wav", ["machine", "speech",  "whistling", "clapping"]],
    ["testDs/20_mch_sp_cp_wh.wav", ["machine", "speech",  "whistling", "clapping"]],
    ["testDs/25_mch_sp_cp_wh.wav", ["machine", "speech",  "whistling", "clapping"]],
])

# with open("testResults.json", "w+") as file:
#     json.dump(results, file)

data, _ = getData("testDs/5_mch_cp.wav")
print(model(data))

# occ_r_a = 0
# s_r_a = 0
# for d in durations:
#     print("### ", d, " ###")
#     for l in labels:
#         # if l == "silence":
#         #     continue
#         # fp_r = results[d][l][fp]
#         # print(fp_r)
#         occ_r = results[d][l][occ]
#         s_r = results[d][l][succ]
#         print("-> ", l, ": ", s_r / float(occ_r))
#         occ_r_a += occ_r
#         s_r_a += s_r

# print(s_r_a / float(occ_r_a))