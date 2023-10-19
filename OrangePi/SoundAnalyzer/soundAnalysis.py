import tflite_runtime.interpreter as tflite
import wave
import numpy as np
import struct

def fromCsv(path: str, delimiter: str):
    mapping = {}

    with open(path, "r") as file:
        lines = file.readlines()
        lines.pop(0)

        for row in lines:
            split = row.strip().split(delimiter)
            mapping[split[1]] = int(split[0])

    return mapping

class SoundAnalyser:
    def __init__(self, pathToModel: str, pathToClasses: str):
        self.classToIndexMapping = fromCsv(pathToClasses, ";")
        self.__interpreter = tflite.Interpreter(pathToModel)
        self.__waveform_input_index = self.__interpreter.get_input_details()[0]['index']
        self.__scores_output_index = self.__interpreter.get_output_details()[0]['index']

    def analyse(self, data):
        self.__interpreter.resize_tensor_input(self.__waveform_input_index, [len(data)], strict=False)
        self.__interpreter.allocate_tensors()
        self.__interpreter.set_tensor(self.__waveform_input_index, data)
        self.__interpreter.invoke()

        scores = self.__interpreter.get_tensor(self.__scores_output_index)[0]

        return { label:scores[index] for (label, index) in self.classToIndexMapping.items() }