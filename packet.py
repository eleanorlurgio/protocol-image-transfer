import math
from numpy import byte


class Packet:

    def __init__(self, sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, data):
        self.sourcePort = int(sourcePort)
        self.destinationPort = int(destinationPort)
        self.seqNum = int(seqNum)
        self.ackNum = int(ackNum)
        self.ackBit = bool(ackBit)
        self.synBit = bool(synBit) 
        self.finBit = bool(finBit)       
        self.checkSum = 0  
        self.data = data

    def setSeqNum(self):
        self.seqNum = 0

    def setAckNum(self):
        self.ackNum = 0

    def setAckBit(self):
        self.ackBit = 1 

    def setSynBit(self, bool):
        self.synBit = bool

    def setFinBit(self):
        self.finBit = 1

    def getDestinationPort(self):
        return self.destinationPort

    def getWindowSize(self):
        return self.windowSize

    def toByteArray(self):

        # Create bytearray object to represent packet
        byteArray = bytearray()

        byteArray[0:2] = self.sourcePort.to_bytes(2, byteorder='big')   # Allocate 2 bytes for sourcePort
        byteArray[2:4] = self.destinationPort.to_bytes(2, byteorder='big')  # Allocate 2 bytes for destinationPort
        byteArray[4:8] = self.seqNum.to_bytes(4, byteorder='big')   # Allocate 4 bytes for seqNum
        byteArray[8:12] = self.ackNum.to_bytes(4, byteorder='big')   # Allocate 4 bytes for ackNum
        byteArray[12:16] = self.ackBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes for ackBit
        byteArray[16:20] = self.synBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes for synBit
        byteArray[20:24] = self.finBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes for finBit
        
        self.checkSum = 0
        byteArray[24:28] = self.checkSum.to_bytes(4, byteorder='big')
        
        byteArray[28:] = bytearray(self.data)   # Allocate bytes 28 onwards to data
        
        # Calculate checksum
        self.checkSum = 0

        for i in range (0, len(byteArray[0:24])):
            self.checkSum += byteArray[i]

        for i in range (0, len(byteArray[28:])):
            self.checkSum += byteArray[28+i]
        
        byteArray[24:28] = self.checkSum.to_bytes(4, byteorder='big')   # Allocate 4 bytes for checkSum

        return byteArray