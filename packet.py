class Packet:

    def __init__(self, sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, data):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        # self.header = bytes(sourcePort) + bytes(destinationPort) + bytes(seqNum) + bytes(ackNum) + bytes(ackBit) + bytes(synBit) + bytes(finBit)
        self.header = str(sourcePort) + str(destinationPort) + str(seqNum) + str(ackNum) + str(ackBit) + str(synBit) + str(finBit)
        self.data = str(data)

        self.packet = self.header + self.data

    # def setHeader(self, seqNum, ackNum, ackBit, synBit, finBit):
    #     seqNum = seqNum
    #     ackNum = ackNum
    #     ackBit = ackBit
    #     synBit = synBit
    #     finBit = finBit

    #     header = bytearray(self.sourcePort, self.destinationPort, seqNum, ackNum, ackBit, synBit, finBit)
    #     return header

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
        print(self.packet)
        return bytearray(self.packet)