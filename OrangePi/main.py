from arduino import Arduino
from soundAnalysis import SoundAnalyser
from audio import Recorder
from setupUtils import waitForArduinoReadiness, checkLabels, getEnvironmentalVariables
import time

modelName, notificationClasses, detectionTreshold, samplingTime = getEnvironmentalVariables()

arduinoConnection = Arduino(3, 0x04)
cnn = SoundAnalyser(f"./models/{modelName}.tflite", f"./models/{modelName}_classes.csv")
audioRecorder = Recorder(16000, "hw:3,0")

checkLabels(cnn, notificationClasses)
waitForArduinoReadiness(arduinoConnection)

# run until terminated 
while True:
    personDetected = False

    data = audioRecorder.record(samplingTime)
    result = cnn.analyse(data)
    detectedClasses = list(filter(lambda label: result[label] >= detectionTreshold, notificationClasses))

    if (len(detectedClasses) > 0):
        waitForArduinoReadiness(arduinoConnection)
        indexes = list(map(lambda label: cnn.classToIndexMapping[label], detectedClasses))
        arduinoConnection.send(f"{','.join(indexes)}:{round(time.time())}")