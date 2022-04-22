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

BUFFER_SIZE = 1024000

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

            # The server responds
            # print("Server has received: " + str(message) + " which is " + str(int.from_bytes(message[5:8], byteorder='big')))

            # print(str(message[1:24]))
            # print(str(message[21:24]))

            print("\n* SERVER HAS RECEIVED *")
            print("Source port: " + str(int.from_bytes(message[1:2], byteorder='big')))
            print("Destination port: " + str(int.from_bytes(message[3:4], byteorder='big')))
            print("Sequence number: " + str(int.from_bytes(message[5:8], byteorder='big')))
            print("Ack number: " + str(int.from_bytes(message[9:12], byteorder='big')))
            print("Ack bit: " + str(int.from_bytes(message[13:16], byteorder='big')))
            print("Syn bit: " + str(int.from_bytes(message[17:20], byteorder='big')))
            print("Fin bit: " + str(int.from_bytes(message[21:24], byteorder='big')))
            # print("Data: " + str(int.from_bytes(message[0:1], byteorder='big')))

            self.serverSend(packet.Packet(8080, 12500, 423894, 1, False, True, False, 1024, "hi"), receivedPacket, serverSocket)

    def serverSend(self, packet, connection, serverSocket):
            serverSocket.sendto(packet.toByteArray(), connection[1])
        
server = Server('127.0.0.1', 8080)
server.serverListen()
