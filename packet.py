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
        # self.data = bytearray(data)

        # self.packet = self.header + self.data

    # def setHeader(self, seqNum, ackNum, ackBit, synBit, finBit):
    #     seqNum = seqNum
    #     ackNum = ackNum
    #     ackBit = ackBit
    #     synBit = synBit
    #     finBit = finBit

    #     header = bytearray(self.sourcePort, self.destinationPort, seqNum, ackNum, ackBit, synBit, finBit)
    #     return header

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

    def setData(data):
        data = data

    def getWindowSize(self):
        return self.windowSize

    def toByteArray(self):

        byteArray = bytearray()

        byteArray[1:2] = self.sourcePort.to_bytes(2, byteorder='big')   # Allocate 2 bytes
        byteArray[3:4] = self.destinationPort.to_bytes(2, byteorder='big')  # Allocate 2 bytes
        byteArray[5:8] = self.seqNum.to_bytes(4, byteorder='big')   # Allocate 4 bytes
        byteArray[9:12] = self.ackNum.to_bytes(4, byteorder='big')   # Allocate 4 bytes
        byteArray[13:16] = self.ackBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes
        byteArray[17:20] = self.synBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes
        byteArray[21:24] = self.finBit.to_bytes(4, byteorder='big')   # Allocate 4 bytes

        return byteArray