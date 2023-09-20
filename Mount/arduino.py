import smbus
import time
from enum import Enum

class Status(Enum):
    READY = 0
    BUSY = 1
    ERROR = 2

class Arduino:
    def __init__(self, i2cNumber: int, address: int):
        self.__bus = smbus.SMBus(i2cNumber)
        self.__address = address

    def status(self):
        return Status(self.__bus.read_byte(self.__address))

    def send(self, message: str):
        length = len(message)
    
        if length > 32:
            raise Exception("Message length exceeds 32 bytes.")
        elif length == 0:
            raise Exception("Nothing to send")
        else:
            data = list(map(self.__toAscii, message))
            firstElement = data[0]
            data.pop(0)
            self.__bus.write_i2c_block_data(self.__address, firstElement, data)

    def __toAscii(self, character: str):
        return ord(character)