import wave
import numpy as np
import struct
import subprocess

class Recorder:
    __file = ".temp/temporary.wav"

    def __init__(self, frequency: int, deviceName: str):
        self.__deviceName = deviceName
        self.__frequency = frequency

    def record(self, duration: int):
        subprocess.run(f"arecord -D {self.__deviceName} -d {duration} -f s16_le -r {self.__frequency} -t wav -c 1 {self.__file}", shell=True)

        wave_data = wave.open(self.__file, "rb")
        frames_count = wave_data.getnframes()
        data = struct.unpack("<" + str(frames_count) + "h", wave_data.readframes(frames_count))
        waveform = np.zeros(len(data), dtype="float32")
       
        for i in range(0, len(data)):
            waveform[i] = data[i] / 32767

        return waveform