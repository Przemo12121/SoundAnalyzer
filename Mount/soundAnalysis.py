import tflite_runtime.interpreter as tflite
import wave
import numpy as np
import struct
import time
import subprocess

class SoundAnalyser:
    def __init__(self, pathToModel: str, pathToClasses: str):
        self.__classes = list(map(lambda line : line.strip(), open(pathToClasses).readlines()))
        self.__interpreter = tflite.Interpreter(pathToModel)
        self.__waveform_input_index = self.__interpreter.get_input_details()[0]['index']
        self.__scores_output_index = self.__interpreter.get_output_details()[0]['index']

    def analyse(self, data):
        self.__interpreter.resize_tensor_input(self.__waveform_input_index, [len(data)], strict=False)
        self.__interpreter.allocate_tensors()
        self.__interpreter.set_tensor(self.__waveform_input_index, data)
        self.__interpreter.invoke()

        scores = self.interpreter.get_tensor(self.__scores_output_index)
        return self.__classes[scores.mean(axis=0).argmax()]