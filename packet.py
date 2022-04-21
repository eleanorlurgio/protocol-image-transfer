class Packet:

    def __init__(self, sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, data):
        self.sourcePort = int(sourcePort)
        self.destinationPort = int(destinationPort)
        # self.header = bytes(sourcePort) + bytes(destinationPort) + bytes(seqNum) + bytes(ackNum) + bytes(ackBit) + bytes(synBit) + bytes(finBit)
        # self.header = str(sourcePort) + str(destinationPort) + str(seqNum) + str(ackNum) + str(ackBit) + str(synBit) + str(finBit)
        self.seqNum = int(seqNum)
        self.ackNum = int(ackNum)
        self.ackBit = int(ackBit)
        self.synBit = int(synBit)
        self.finBit = int(finBit)
        self.data = str(data)

        # self.packet = self.header + self.data

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
        # print(self.packet)
        byteArray = bytearray()
        byteArray[1:2] = self.sourcePort.to_bytes(2, byteorder='big')
        byteArray[3:4] = self.destinationPort.to_bytes(2, byteorder='big')
        byteArray[5:8] = self.seqNum.to_bytes(4, byteorder='big')
        byteArray[9:12] = self.ackNum.to_bytes(4, byteorder='big')
        byteArray[13:16] = self.ackBit.to_bytes(4, byteorder='big')
        byteArray[17:20] = self.synBit.to_bytes(4, byteorder='big')
        byteArray[21:24] = self.finBit.to_bytes(4, byteorder='big')
        # self.sourcePort.to_bytes(2, byteorder='big') + self.destinationPort.to_bytes(2, byteorder='big') + self.seqNum.to_bytes(4, byteorder='big') + self.ackNum.to_bytes(4, byteorder='big') + self.synBit.to_bytes(4, byteorder='big') + self.finBit.to_bytes(4, byteorder='big')
        return byteArray