import wave
import subprocess
import time

freq = 16000
time.sleep(5)

# for i in range(620, 635):
#     print(i)    
#     # duration = i % 11 + 5
#     duration = 10
#     subprocess.run(f"arecord -q -f S16_LE -r {freq} -d {duration} ./data/training/machine_speech/{i+1}.wav -c 1", shell=True)

for i in range(635, 640):
    print(i)    
    # duration = i % 11 + 5
    duration = 10
    subprocess.run(f"arecord -q -f S16_LE -r {freq} -d {duration} ./data/validation/machine_speech/{i+1}.wav -c 1", shell=True)
    

print("finished")