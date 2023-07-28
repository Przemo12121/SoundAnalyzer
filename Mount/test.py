import tflite_runtime.interpreter as tflite
import wave
import numpy as np
import struct

interpreter = tflite.Interpreter("./models/test_model.tflite")

wave_data = wave.open("./files/meow.wav", "rb")

frames_count = wave_data.getnframes()
data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
waveform = np.zeros(len(data), dtype="float32")
for i in range(0, len(data)):
    waveform[i] = data[i] / 32767


input_details = interpreter.get_input_details()
waveform_input_index = input_details[0]['index']
output_details = interpreter.get_output_details()
scores_output_index = output_details[0]['index']

# # # Input: 3 seconds of silence as mono 16 kHz waveform samples.
# waveform = np.zeros(3 * 16000, dtype=np.float32)

interpreter.resize_tensor_input(waveform_input_index, [len(waveform)], strict=False)
interpreter.allocate_tensors()
interpreter.set_tensor(waveform_input_index, waveform)
interpreter.invoke()
scores = interpreter.get_tensor(scores_output_index)

class_names = list(map(lambda line : line.strip(), open('./models/classes.csv').readlines()))
for i in range(0, len(class_names)):
    if (scores[0][i] > 0):
        print(f"{scores[0][i]} - {class_names[i]}")

# print(scores)
print(class_names[scores.mean(axis=0).argmax()])