class Packet:

    def __init__(self, sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, data):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.header = str(self.sourcePort) + str(self.destinationPort) + str(seqNum) + str(ackNum) + str(ackBit) + str(synBit) + str(finBit)
        # self.header = (self.sourcePort) + (self.destinationPort) + (seqNum) + (ackNum) + (ackBit) + (synBit) + (finBit)
        self.data = data

    def setHeader(self, seqNum, ackNum, ackBit, synBit, finBit):
        seqNum = seqNum
        ackNum = ackNum
        ackBit = ackBit
        synBit = synBit
        finBit = finBit

        header = bytearray(self.sourcePort, self.destinationPort, seqNum, ackNum, ackBit, synBit, finBit)
        return header

    def setSeqNum():
        seqNum = 0

    def setAckNum():
        ackNum = 0

    def setAckBit():
        ackBit = 1 

    def setSynBit():
        synBit = 1

    def setFinBit():
        finBit = 1

    def setData(data):
        data = data

    def toByteArray(self):
        return bytearray(self.header)