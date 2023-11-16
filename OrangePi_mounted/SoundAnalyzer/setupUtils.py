import time
from arduino import Arduino, Status
from soundAnalysis import SoundAnalyser
from dotenv import load_dotenv
import os

def getEnvironmentalVariables():
    load_dotenv()
    return os.getenv("MODEL_NAME"), \
        os.getenv("NOTIFICATION_CLASSES").split(","), \
        float(os.getenv("DETECTION_TRESHOLD")), \
        int(os.getenv("AUDIO_SAMPLING_TIME_SECONDS")), \
        int(os.getenv("AUDIO_SAMPLING_CHUNK")), \
        int(os.getenv("RECORDING_FREQUENCY"))

def waitForArduinoReadiness(connection: Arduino):
    for _ in range(10):
        status = connection.status()

        if status == Status.READY:
            return
        elif status == Status.BUSY:
            time.sleep(1)
            continue
        else: # Status.ERROR
            raise Exception("Arduino responded with error status.")

    raise Exception("Arduino busy for too long.")

def checkLabels(soundAnalyzer: SoundAnalyser, targetLabels: list):
    keys = list(soundAnalyzer.classToIndexMapping.keys())

    notOutputedLabels = list(filter(lambda item : item not in keys, targetLabels))

    if len(notOutputedLabels) > 0:
        raise Exception(f"Tensorflow model does not output probabilities for labels: {', '.join(notOutputedLabels)}.")