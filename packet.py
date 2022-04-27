class Packet:

    def __init__(self, sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit,  windowSize, data):
        self.sourcePort = int(sourcePort)
        self.destinationPort = int(destinationPort)
        self.seqNum = int(seqNum)
        self.ackNum = int(ackNum)
        self.ackBit = bool(ackBit)
        self.synBit = bool(synBit) 
        self.finBit = bool(finBit)       
        self.windowSize = int(windowSize)   
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
        if(type(self.data) is bytes):
            byteArray[24:] = self.data   # Allocate the rest of the bytes to data

        return byteArray