from arduino import Arduino
from soundAnalysis import SoundAnalyser
from audio import Recorder
from setupUtils import waitForArduinoReadiness, checkLabels, getEnvironmentalVariables
import time

modelName, notificationClasses, detectionTreshold, \
    samplingTime, samplingChunk, recordingFrequency = getEnvironmentalVariables()

arduinoConnection = Arduino(3, 0x04)
cnn = SoundAnalyser(f"/root/SoundAnalyzer/models/{modelName}.tflite", f"/root/SoundAnalyzer/models/{modelName}_classes.csv")
audioRecorder = Recorder(recordingFrequency, "hw:3,0")

checkLabels(cnn, notificationClasses)
waitForArduinoReadiness(arduinoConnection)

# run until terminated 
while True:
    resultsOverChunks = { label:0 for label in notificationClasses }

    # analyse data from requested sampling chunks with requested sampling time per chunk 
    for _ in range(samplingChunk):
        data = audioRecorder.record(samplingTime)
        result = cnn.analyse(data)

        # pick maximum values
        for label in notificationClasses:
            resultsOverChunks[label] = max(resultsOverChunks[label], result[label])            

    # filter results based on requested detection treshold
    detectedClasses = list(
        filter(
            lambda label: resultsOverChunks[label] >= detectionTreshold, 
            notificationClasses))

    # notify
    if (len(detectedClasses) > 0):
        waitForArduinoReadiness(arduinoConnection)
        
        indexes = list(
            map(
                lambda label: str(cnn.classToIndexMapping[label]), 
                detectedClasses))

        arduinoConnection.send(f"{','.join(indexes)}:{round(time.time())}")