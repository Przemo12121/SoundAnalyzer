import wave
import subprocess
import time

freq = 16000
time.sleep(5)

for i in range(150, 200):
    print(i)
    duration = i % 11 + 5
    subprocess.run(f"arecord -q -f S16_LE -r {freq} -d {duration} ./data/machine_speach/{i+1}.wav -c 1", shell=True)

print("finished")