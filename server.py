# p2p.py>

import random
from socket import *
from email import message, message_from_bytes
import sys
from threading import Thread
import socket
from time import sleep, time
from cv2 import cv2
import packet

HEADER_SIZE = 24
DATA_SIZE = 1000000
BUFFER_SIZE = HEADER_SIZE + DATA_SIZE

class Server:

    def __init__(self, sourceIP, sourcePort):
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort

    # Listen for incoming requests
    def serverListen(self):

        # Create a UDP socket with use of SOCK_DGRAM for UDP packets
        serverSocket = socket.socket(family=AF_INET, type=SOCK_DGRAM)

        # Assign IP address and port number to socket
        serverSocket.bind((self.sourceIP, self.sourcePort))

        while True:
            # Receive the client packet along with the address it is coming from
            receivedPacket = serverSocket.recvfrom(BUFFER_SIZE)
            message = receivedPacket[0]
            address = receivedPacket[1]

            sourcePort = int.from_bytes(message[0:2], byteorder='big')
            destPort = int.from_bytes(message[2:4], byteorder='big')
            seqNum = int.from_bytes(message[4:8], byteorder='big')
            ackNum = int.from_bytes(message[8:12], byteorder='big')
            ackBit = int.from_bytes(message[12:16], byteorder='big')
            synBit = int.from_bytes(message[16:20], byteorder='big')
            finBit = int.from_bytes(message[20:24], byteorder='big')
            data = int.from_bytes(message[24:], byteorder='big')

            # Set message to the data to be sent back
            # my_img = cv2.imread("image_white.png", cv2.IMREAD_GRAYSCALE)

            print("\n* SERVER HAS RECEIVED *")
            print("Source port: " + str(sourcePort))
            print("Destination port: " + str(destPort))
            print("Sequence number: " + str(seqNum))
            print("Ack number: " + str(ackNum))
            print("Ack bit: " + str(ackBit))
            print("Syn bit: " + str(synBit))
            print("Fin bit: " + str(finBit))
            print("Data: " + str(data))
            # print("Data: " + str(int.from_bytes(message[0:1], byteorder='big')))

            # self.serverSend(message, address, serverSocket)

            # If synBit == 1
            if synBit == 1:
                print("Handshake 1/3 complete")

                # sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, windowSize, data
                serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), True, True, False, 1024, 0)
                serverSocket.sendto(serverPacket.toByteArray(), address)
            
            # If ackBit == 1
            if ackBit == 1:
                print("Handshake 3/3 complete")
                print("CONNECTION ESTABLISHED")

                # Send packet with data
                serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), False, False, False, 1024, 123456789)
                serverSocket.sendto(serverPacket.toByteArray(), address)


server = Server('127.0.0.1', 8080)
server.serverListen()
