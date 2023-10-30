import wave
import numpy as np
import struct
import subprocess
from pydub import AudioSegment

class Recorder:
    __file = ".temp.wav"

    def __init__(self, frequency: int, deviceName: str):
        self.__deviceName = deviceName
        self.__frequency = frequency

    def record(self, duration: int):
        subprocess.run(f"arecord -D {self.__deviceName} -d {duration} -f s16_le -r {self.__frequency} -t wav -c 1 {self.__file}", shell=True)

        data = AudioSegment.from_file(self.__file, format='wav', frame_rate=44100)

        # audio preprocessing - resample to 16kHz and normalize values between [-1.0, 1.0]
        data = data.set_frame_rate(16000)
        data = data.get_array_of_samples()
        return np.array(data).astype(np.float32) / 32767