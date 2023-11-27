import matplotlib.pyplot as plt
import json
import os
import tensorflow as tf
import wave
import struct
import numpy

modelName = "sv11"
model = tf.saved_model.load(f"./models/{modelName}")
freq = 16000

def plotData(path):
    # print(path)


    wave_data = wave.open(path, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = numpy.zeros(len(data), dtype="float32")
    
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767

    waveform = waveform[16000:16000*6+1]
    result = model(waveform).numpy()[0]
    result = [str(round(r, 2)) for r in result]

    time = int(len(waveform) / freq)
    ax = plt.gca()
    ax.set_ylim([-1.0, 1.0])
    ax.set_xlim([0, len(waveform)])
    plt.xticks([t * freq for t in range(time+1)], range(time+1))
    plt.ylabel("Wartość sygnału")
    plt.xlabel("Czas [s]")
    plt.plot(waveform)
    plt.show()

    # print(result[0])
    print()
    print("{")
    print(f"  clapping: {result[0]}"), 
    print(f"  machine: {result[1]}"), 
    print(f"  silence: {result[2]}"), 
    print(f"  speech: {result[3]}"), 
    print(f"  whistling: {result[4]}") 
    print("}")
    # print({ "clapping": result[0], "machine": result[1], "silence": result[2], "speech": result[3], "whistling": result[4] })
    print()

plotData("m_w_short.wav")

# with open(f"models/{modelName}/history.json", "r") as historyFile:
    
    # history = json.load(historyFile)
    # valuesAcc = history["accuracy"]
    # valuesVal = history["val_accuracy"]
    # length = len(valuesAcc)
    # figureAcc = plt.figure()
    # ax = figureAcc.add_subplot(111)
    # plt.ylabel("Trafność modelu [%]")
    # plt.xlabel("Epoka")
    # plt.plot(range(length), valuesAcc, markevery=[length-1], marker="o")
    # plt.plot(range(length), valuesVal, markevery=[length-1], marker="o")
    # plt.legend(["trening", "walidacja"], loc="lower right")
    # ax.text(length-1, valuesAcc[-1]+0.01, round(valuesAcc[-1], 2), ha="center")
    # ax.text(length, valuesVal[-1]-0.03, round(valuesVal[-1], 2), ha="center")
    # plt.show()

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

    # loss function
    # plt.plot(history["loss"])
    # plt.plot(history["val_loss"])
    # # plt.title("Wykres wartości funkcji straty modelu")
    # plt.ylabel("Funkcja straty")
    # plt.xlabel("Epoka")
    # plt.legend(["trening", "walidacja"], loc="upper left")
    # plt.show()