# p2p.py>

from asyncio.windows_events import NULL
import math
from msilib.schema import File
import random
from socket import *
from email import message, message_from_bytes
import sys
from threading import Thread
import socket
from time import sleep, time
from cv2 import cv2
from numpy import size
import numpy
import packet

HEADER_SIZE = 28
DATA_SIZE = 996
BUFFER_SIZE = HEADER_SIZE + DATA_SIZE

sys.setrecursionlimit(15000)

class Server:

    def __init__(self, sourceIP, sourcePort):
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort
        self.connection = False
        self.closing = False

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
            checkSum = int.from_bytes(message[24:28], byteorder='big')
            data = int.from_bytes(message[28:], byteorder='big')

            # Calculate checksum
            validateCheckSum = 0

            for i in range (0, len(message[0:24])):
                validateCheckSum += message[i]

            for i in range (0, len(message[28:])):
                validateCheckSum += message[28+i]

            # Display packet contents in terminal
            print("\n* SERVER HAS RECEIVED *")
            print("Source port: " + str(sourcePort))
            print("Destination port: " + str(destPort))
            print("Sequence number: " + str(seqNum))
            print("Ack number: " + str(ackNum))
            print("Ack bit: " + str(ackBit))
            print("Syn bit: " + str(synBit))
            print("Fin bit: " + str(finBit))
            print("Checksum: " + str(checkSum))
            print("Data: " + str(data))
            if (checkSum == validateCheckSum):
                print("SUCCESSFUL CHECKSUM")

            # Check bits of received packet to respond accordingly

            # HANDSHAKE TO CONNECT

            # Complete handshake 1/3
            if (synBit == 1) and (self.connection == False) and (self.closing == False):
                print("Opening handshake 1/3 complete")

                # Send response packet
                serverPacket = packet.Packet(self.sourcePort, sourcePort, random.randint(0, 2147483647), (seqNum + 1), True, True, False, NULL)
                serverSocket.sendto(serverPacket.toByteArray(), address)
            
            # Complete handshake 3/3
            if (ackBit == 1) and (self.connection == False) and (self.closing == False):
                print("Opening handshake 3/3 complete")
                print("CONNECTION ESTABLISHED")
                self.connection = True

                # Read image to be sent as data in the packet
                with open("Rainbow.jpg", "rb") as image:
                    file = image.read()
                    img = bytearray(file)

                # Calculate how many packets need to be sent
                noOfPackets = math.ceil(len(img) / DATA_SIZE)
                print("The number of data packets is", noOfPackets)

                startByte = 0

                self.sendImage(serverSocket, message, address, img, startByte, noOfPackets)

            # Send image
            elif (ackBit == 1) and (self.connection == True) and (self.closing == False):
                # Acknowledgement packet received from client, so send next data packet
                print("Acknowledgement packet received")
                startByte += DATA_SIZE
                noOfPackets -= 1
                self.sendImage(serverSocket, message, address, img, startByte, noOfPackets)
            
            if (ackBit == 1) and (self.connection == True) and (self.closing == True):
                # Acknowledge closing packet 2/4
                print("Closing handshake 2/4 complete")
                
            if (ackBit == 1) and (finBit == 1) and (self.connection == True) and (self.closing == True):
                print("Closing handshake 3/4 complete")
                # Close connection 4/4
                closingPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[8:12], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, True, NULL)
                serverSocket.sendto(closingPacket.toByteArray(), address)

                # Close socket and terminate
                serverSocket.close()
                exit()

    def sendImage(self, serverSocket, message, address, img, startByte, noOfPackets):

        if noOfPackets > 0:
            # Send response packet with data
            serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[8:12], byteorder='big'), int.from_bytes(message[4:8], byteorder='big'), True, False, False, img[startByte:(startByte+DATA_SIZE)])
            serverSocket.sendto(serverPacket.toByteArray(), address)
        else:
            # Close connection 1/4
            print("Closing connection")
            self.closing = True
            closePacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[8:12], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, True, NULL)
            serverSocket.sendto(closePacket.toByteArray(), address)

# Initialise and start server
server = Server('0.0.0.0', 8080)
server.serverListen()
