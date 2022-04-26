# p2p.py>

from asyncio.windows_events import NULL
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

    # Server listens and responds
    def serverListen(self):
        # Create a UDP socket with use of SOCK_DGRAM for UDP packets
        serverSocket = socket.socket(family=AF_INET, type=SOCK_DGRAM)

        # Assign IP address and port number to socket
        serverSocket.bind((self.sourceIP, self.sourcePort))

        # Server listens continuously
        while True:
            # Receive the client packet along with the client address
            receivedPacket = serverSocket.recvfrom(BUFFER_SIZE)

            # Split received packet into contents and address
            message = receivedPacket[0]
            address = receivedPacket[1]

            # Read bytes
            sourcePort = int.from_bytes(message[0:2], byteorder='big')
            destPort = int.from_bytes(message[2:4], byteorder='big')
            seqNum = int.from_bytes(message[4:8], byteorder='big')
            ackNum = int.from_bytes(message[8:12], byteorder='big')
            ackBit = int.from_bytes(message[12:16], byteorder='big')
            synBit = int.from_bytes(message[16:20], byteorder='big')
            finBit = int.from_bytes(message[20:24], byteorder='big')
            data = int.from_bytes(message[24:], byteorder='big')

            # Display packet contents in terminal
            print("\n* SERVER HAS RECEIVED *")
            print("Source port: " + str(sourcePort))
            print("Destination port: " + str(destPort))
            print("Sequence number: " + str(seqNum))
            print("Ack number: " + str(ackNum))
            print("Ack bit: " + str(ackBit))
            print("Syn bit: " + str(synBit))
            print("Fin bit: " + str(finBit))
            print("Data: " + str(data))

            # Check bits of received packet to respond accordingly

            # Complete handshake 1/3
            if synBit == 1:
                print("Handshake 1/3 complete")

                # Send response packet
                serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), True, True, False, 1024, NULL)
                serverSocket.sendto(serverPacket.toByteArray(), address)
            
            # Complete handshake 3/3
            if ackBit == 1:
                print("Handshake 3/3 complete")
                print("CONNECTION ESTABLISHED")

                # Read image to be sent as data in the packet
                img = cv2.imread("image_black.png", cv2.IMREAD_GRAYSCALE)

                # Send response packet with data
                serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), False, False, False, 1024, img)
                serverSocket.sendto(serverPacket.toByteArray(), address)

# Initialise and start server
server = Server('127.0.0.1', 8080)
server.serverListen()
