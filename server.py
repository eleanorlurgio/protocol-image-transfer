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

BUFFER_SIZE = 24

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

            # Set message to the data to be sent back
            # my_img = cv2.imread("image_white.png", cv2.IMREAD_GRAYSCALE)

            print("\n* SERVER HAS RECEIVED *")
            print("Source port: " + str(int.from_bytes(message[0:2], byteorder='big')))
            print("Destination port: " + str(int.from_bytes(message[2:4], byteorder='big')))
            print("Sequence number: " + str(int.from_bytes(message[4:8], byteorder='big')))
            print("Ack number: " + str(int.from_bytes(message[8:12], byteorder='big')))
            print("Ack bit: " + str(int.from_bytes(message[12:16], byteorder='big')))
            print("Syn bit: " + str(int.from_bytes(message[16:20], byteorder='big')))
            print("Fin bit: " + str(int.from_bytes(message[20:24], byteorder='big')))
            # print("Data: " + str(int.from_bytes(message[0:1], byteorder='big')))

            self.serverSend(message, address, serverSocket)

    def serverSend(self, message, address, serverSocket):

        # Check bits of received packet

        # If synBit == 1
        if int.from_bytes(message[16:20], byteorder='big') == 1:
            print("Handshake 1/3 complete")

            # sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, windowSize, data
            serverPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), random.randint(0, 2147483647), (int.from_bytes(message[4:8], byteorder='big') + 1), True, True, False, 1024, 0)
            serverSocket.sendto(serverPacket.toByteArray(), address)
        
        # If ackBit == 1
        if int.from_bytes(message[12:16], byteorder='big') == 1:
            print("Handshake 3/3 complete")
            print("CONNECTION ESTABLISHED")

            


server = Server('127.0.0.1', 8080)
server.serverListen()
