# p2p.py>

from asyncio.windows_events import NULL
import math
import random
from socket import *
from email import message, message_from_bytes
import sys
from threading import Thread
import socket
from time import sleep, time
from cv2 import cv2
from numpy import size
import packet

HEADER_SIZE = 24
DATA_SIZE = 60
BUFFER_SIZE = HEADER_SIZE + DATA_SIZE


class Server:

    def __init__(self, sourceIP, sourcePort):
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort
        self.connection = False

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

            # HANDSHAKE TO CONNECT

            # Complete handshake 1/3
            if synBit == 1:
                print("Handshake 1/3 complete")

                # Send response packet
                serverPacket = packet.Packet(self.sourcePort, sourcePort, random.randint(0, 2147483647), (seqNum + 1), True, True, False, 1024, NULL)
                serverSocket.sendto(serverPacket.toByteArray(), address)
            
            # Complete handshake 3/3
            if (ackBit == 1) and (self.connection == False):
                print("Handshake 3/3 complete")
                print("CONNECTION ESTABLISHED")

                self.connection = True

                # Read image to be sent as data in the packet
                img = cv2.imread("Rainbow.jpg", cv2.IMREAD_GRAYSCALE)
                print("image type is", type(img))
                noOfPackets = math.ceil(len(str(img).encode("utf-8")) / DATA_SIZE)
                print("packet no is ", noOfPackets)

                startByte = 0

                self.sendImage(serverSocket, message, address, img, startByte, noOfPackets)

                # Read image to be sent as data in the packet
                # img = cv2.imread("image_black.png", cv2.IMREAD_GRAYSCALE)

                # # Send response packet with data
                # serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), False, False, False, 1024, img)
                # serverSocket.sendto(serverPacket.toByteArray(), address)

                # SEND IMAGE
            if (ackBit == 1) and (self.connection == True):
                        # Close connection 1/4
                print("acknowledgement received")
                startByte += 60
                noOfPackets -= 1
                self.sendImage(serverSocket, message, address, img, startByte, noOfPackets)
                

            # HANDSHAKE TO DISCONNECT

    def sendImage(self, serverSocket, message, address, img, startByte, noOfPackets):


        # print(size(img))

        # noOfPackets = math.ceil(size(img) / DATA_SIZE)

        print(noOfPackets)

        # print(str(img).encode("utf-8"))
        # print(len(str(img).encode("utf-8")))
        # print(size(img[startByte:(startByte+60)]))
        print(len(str(img).encode("utf-8")))
        print(str(img)[180:240].encode("utf-8"))

        if noOfPackets > 1:
            # Send response packet with data
            serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), False, False, False, 1024, str(img)[startByte:(startByte+60)].encode("utf-8"))
            serverSocket.sendto(serverPacket.toByteArray(), address)

        # elif noOfPackets == 1:
        #     # Send response packet with data
        #     serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), False, False, False, 1024, img[startByte:])
        #     serverSocket.sendto(serverPacket.toByteArray(), address)

        else:
            # Close connection 1/4
            print("closing connection?")
            closePacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, True, 1024, NULL)
            print("sending close")
            serverSocket.sendto(closePacket.toByteArray(), address)

# Initialise and start server
server = Server('127.0.0.1', 8080)
server.serverListen()
