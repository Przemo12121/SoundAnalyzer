from arduino import Arduino, Status
from soundAnalysis import SoundAnalyser
from audio import Recorder
import time

def waitForArduinoReadiness(connection: Arduino):
    for i in range(10):
        status = connection.status()

        if status == Status.READY:
            return
        elif status == Status.BUSY:
            time.sleep(1)
            continue
        else: # Status.ERROR
            raise Exception("Arduino responded with error status.")

    raise Exception("Arduino busy for too long.")


#TODO: read i2c bus number and address from .env 
arduinoConnection = Arduino(3, 0x04)
cnn = SoundAnalyser("./models/sound_analyzer_v1.tflite", "./models/classes.csv")
audioRecorder = Recorder(16000, "hw:3,0")
classesToNotify = ["speech", "walk"]

waitForArduinoReadiness(arduinoConnection)

#TODO: test
# run until terminated 
while True:
    personDetected = False

    for i in range(6):
        data = audioRecorder.record(10)
        analysisResult = cnn.analyse(data)

        # TODO: Read detection classes from config, adjust expression
        personDetected = not personDetected and analysisResult in classesToNotify
    
    if personDetected:
        waitForArduinoReadiness(arduinoConnection)
        arduinoConnection.send(f"speech,{time.time()}")