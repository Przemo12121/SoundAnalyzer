import tflite_runtime.interpreter as tflite
import wave
import numpy as np
import struct
# import os
import time
import subprocess

fileName = "test.wav"
interpreter = tflite.Interpreter("./models/test_model.tflite")

for i in range(1):
    record_start = time.time()
    subprocess.run(f"arecord -D hw:3,0 -d 5 -f s16_le -r 16000 -t wav -c 1 {fileName}", shell=True)
    record_end = time.time()

    file_read_start = time.time()
    wave_data = wave.open(fileName, "rb")
    frames_count = wave_data.getnframes()
    data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
    waveform = np.zeros(len(data), dtype="float32")
    for i in range(0, len(data)):
        waveform[i] = data[i] / 32767
    file_read_end = time.time()

    ml_start = time.time()
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
        if (scores[0][i] > 0.5):
            print(f"{scores[0][i]} - {class_names[i]}")
    ml_end = time.time()

    # print(scores)
    print(class_names[scores.mean(axis=0).argmax()])


    print("measurements:")
    print(ml_end - record_start)
    print(record_end - record_start)
    print(file_read_end - file_read_start)
    print(ml_end - ml_start)
    print(f"len: {len(data)}")
    time.sleep(2)