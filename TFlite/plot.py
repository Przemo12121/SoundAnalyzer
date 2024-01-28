import matplotlib.pyplot as plt
import json
import os
import tensorflow as tf
import wave
import struct
import numpy

modelName = "sv12"
model = tf.saved_model.load(f"./models/{modelName}")
freq = 16000

succ = "successes"
occ = "occurences"
fp = "falsePositives"
miss = "misstakes"

# with open(f"testResults.json", "r") as resultsFile:
#     r = json.load(resultsFile)

#     silence = []
#     speech = []
#     machine = []
#     whistling = []
#     clapping = []
#     x = []

#     for d in r:
#         x.append(int(d))
#         silence.append( r[d]["silence"][succ] / float(r[d]["silence"][occ]) * 100 )
#         machine.append( r[d]["machine"][succ] / float(r[d]["machine"][occ]) * 100 )
#         speech.append( r[d]["speech"][succ] / float(r[d]["speech"][occ]) * 100 )
#         clapping.append( r[d]["clapping"][succ] / float(r[d]["clapping"][occ]) * 100 )
#         whistling.append( r[d]["whistling"][succ] / float(r[d]["whistling"][occ]) * 100 )

#     print(speech)
#     figureAcc = plt.figure()
#     ax = figureAcc.add_subplot(111)
#     plt.ylabel("Skuteczność klasyfikacji klasy [%]")
#     plt.xlabel("Czas sygnału wejściowego [s]")
#     plt.plot(x, silence, markevery=range(0, len(x)), marker="o")
#     plt.plot(x, machine, markevery=range(0, len(x)), marker="o")
#     plt.plot(x, speech, markevery=range(0, len(x)), marker="o")
#     plt.plot(x, clapping, markevery=range(0, len(x)), marker="o")
#     plt.plot(x, whistling, markevery=range(0, len(x)), marker="o")
#     plt.legend(["cisza", "maszyny", "mowa", "klaskanie", "gwizdanie"], loc="lower left")
#     plt.xticks(x)
#     # ax.text(length-1, valuesAcc[-1]+0.01, round(valuesAcc[-1], 2), ha="center")
#     # ax.text(length, valuesVal[-1]-0.03, round(valuesVal[-1], 2), ha="center")
#     plt.show()


# def plotData(path):
#     # print(path)

#     wave_data = wave.open(path, "rb")
#     frames_count = wave_data.getnframes()
#     data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
#     waveform = numpy.zeros(len(data), dtype="float32")
    
#     for i in range(0, len(data)):
#         waveform[i] = data[i] / 32767

#     waveform = waveform[10000:100000]
#     result = model(waveform).numpy()[0]
#     result = [str(round(r, 2)) for r in result]

#     time = int(len(waveform) / freq)
#     ax = plt.gca()
#     ax.set_ylim([-1.0, 1.0])
#     ax.set_xlim([0, len(waveform)])
#     plt.xticks([t * freq for t in range(time+1)], range(time+1))
#     plt.ylabel("Wartość sygnału")
#     plt.xlabel("Czas [s]")
#     plt.plot(waveform)
#     plt.show()

#     # print(result[0])
#     print()
#     print("{")
#     print(f"  clapping: {result[0]}"), 
#     print(f"  machine: {result[1]}"), 
#     print(f"  silence: {result[2]}"), 
#     print(f"  speech: {result[3]}"), 
#     print(f"  whistling: {result[4]}") 
#     print("}")
#     # print({ "clapping": result[0], "machine": result[1], "silence": result[2], "speech": result[3], "whistling": result[4] })
#     print()

# plotData("testDs/10_sil_sp_cp_wh.wav")

# with open(f"models/{modelName}/history.json", "r") as historyFile:
    
#     history = json.load(historyFile)
#     valuesAcc = numpy.array(history["accuracy"]) * 100
#     valuesVal = numpy.array(history["val_accuracy"]) * 100
#     # valuesAcc = history["accuracy"]
#     # valuesVal = history["val_accuracy"]
#     length = len(valuesAcc)
#     figureAcc = plt.figure()
#     ax = figureAcc.add_subplot(111)
#     plt.ylabel("Trafność modelu [%]")
#     plt.xlabel("Epoka")
#     plt.plot(range(length), valuesAcc, markevery=[length-1], marker="o")
#     plt.plot(range(length), valuesVal, markevery=[length-1], marker="o")
#     plt.legend(["trening", "walidacja"], loc="lower right")
#     ax.text(length-1, valuesAcc[-1]+1, round(valuesAcc[-1], 0), ha="center")
#     ax.text(length, valuesVal[-1]-3, round(valuesVal[-1], 0), ha="center")
#     plt.show()

    # history = json.load(historyFile)
    # valuesAcc = history["loss"]
    # valuesVal = history["val_loss"]
    # length = len(valuesAcc)
    # figureAcc = plt.figure()
    # ax = figureAcc.add_subplot(111)
    # plt.ylabel("Wartość funkcji straty")
    # plt.xlabel("Epoka")
    # plt.plot(range(length), valuesAcc, markevery=[length-1], marker="o")
    # plt.plot(range(length), valuesVal, markevery=[length-1], marker="o")
    # plt.legend(["trening", "walidacja"], loc="upper right")
    # ax.text(length-1, valuesAcc[-1]+0.03, round(valuesAcc[-1], 2), ha="center")
    # ax.text(length, valuesVal[-1]+0.022, round(valuesVal[-1], 2), ha="center")
    # plt.show()

    # # loss function
    # plt.plot(history["loss"])
    # plt.plot(history["val_loss"])
    # # plt.title("Wykres wartości funkcji straty modelu")
    # plt.ylabel("Funkcja straty")
    # plt.xlabel("Epoka")
    # plt.legend(["trening", "walidacja"], loc="upper left")
    # plt.show()