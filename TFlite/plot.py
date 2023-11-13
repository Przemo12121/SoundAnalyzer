import matplotlib.pyplot as plt
import json
import os

modelName = "sound_analyzer_v2"

with open(f"models/{modelName}/history.json", "r") as historyFile:
    history = json.load(historyFile)

    # accuracy
    plt.plot(history["accuracy"])
    plt.plot(history["val_accuracy"])
    plt.title("Wykres skuteczności modelu")
    plt.ylabel("Trafność modelu [%]")
    plt.xlabel("Epoka")
    plt.legend(["trening", "walidacja"], loc="upper left")
    plt.show()

    # loss function
    plt.plot(history["loss"])
    plt.plot(history["val_loss"])
    plt.title("Wykres wartości funkcji straty modelu")
    plt.ylabel("Funkcja straty")
    plt.xlabel("Epoka")
    plt.legend(["trening", "walidacja"], loc="upper left")
    plt.show()