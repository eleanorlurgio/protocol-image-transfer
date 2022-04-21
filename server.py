# p2p.py>

import random
from socket import *
from email import message
import sys
from threading import Thread
import socket
from time import sleep, time
from cv2 import cv2
import packet

BUFFER_SIZE = 1024000

class Server:
    # Listen for incoming requests
    def serverListen(self):

        # Create a UDP socket with use of SOCK_DGRAM for UDP packets
        serverSocket = socket.socket(family=AF_INET, type=SOCK_DGRAM)

        # Assign IP address and port number to socket
        serverSocket.bind(('127.0.0.1', 12501))

        while True:
            # Receive the client packet along with the address it is coming from
            connection = serverSocket.recvfrom(BUFFER_SIZE)
            message = connection[0]
            address = connection[1]

            # Set message to the data to be sent back
            # my_img = cv2.imread("image_white.png", cv2.IMREAD_GRAYSCALE)

            # The server responds
            print("                                      "+ ": " + str(message))

            self.serverSend(packet.Packet(12501, 12500, 0, 0, 0, 0, 0, "data"), connection, serverSocket)

    def serverSend(self, packet, connection, serverSocket):
            serverSocket.sendto(packet.toByteArray(), connection[1])
        
server = Server()
server.serverListen()
