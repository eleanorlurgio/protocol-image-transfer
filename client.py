# import server
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

class Client:

	def __init__(self, sourceIP, sourcePort):
		self.sourceIP = sourceIP
		self.sourcePort = sourcePort

	# The connection is defined by a tuple (source IP, source port, destination IP, destination port)
	# Send data
	def clientSend(self, packet):
		# Create a UDP socket
		UDP_IP_ADDRESS = self.sourceIP
		UDP_PORT_NO = 8080

		# Request message from user client
		# Message = str.encode("request photo")

		# Read image
		# my_img = cv2.imread("image_black.png", cv2.IMREAD_GRAYSCALE)
		# packet.setData(my_img)
		# print(my_img)
		# cv2.imshow('My image', my_img)
		# cv2.waitKey(0)

		# sleep(1000)

		# Create a socket with a 1s timeout
		clientSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		clientSock.settimeout(2.0)

		# Send data to client
		# print('Ping %d %s' % (1,Message.decode()))

		while True:
			# Send the message using the clientSock
			# clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
			# bytearray(packet.toByteArray(), 'utf-8')
			clientSock.sendto(packet.toByteArray(), (UDP_IP_ADDRESS, UDP_PORT_NO))

			# Receive response
			print('waiting to receive')

			# Get the response & extract data
			try:
				serverPacket = clientSock.recvfrom(1024)
			except TimeoutError:
				print("timeout")
				sleep(0.1)
				continue
			except ConnectionResetError:
				print("server not up")
				sleep(0.1)
				continue
			break

		message = serverPacket[0]
		address = serverPacket[1]

		# print(str(serverPacket))
		# print('client received: ' + str(img))

		print("\n* CLIENT HAS RECEIVED *")
		print("Source port: " + str(int.from_bytes(message[0:2], byteorder='big')))
		print("Destination port: " + str(int.from_bytes(message[2:4], byteorder='big')))
		print("Sequence number: " + str(int.from_bytes(message[4:8], byteorder='big')))
		print("Ack number: " + str(int.from_bytes(message[8:12], byteorder='big')))
		print("Ack bit: " + str(int.from_bytes(message[12:16], byteorder='big')))
		print("Syn bit: " + str(int.from_bytes(message[16:20], byteorder='big')))
		print("Fin bit: " + str(int.from_bytes(message[20:24], byteorder='big')))
            # print("Data: " + str(int.from_bytes(message[0:1], byteorder='big')))

		# Close the socket
		print('closing socket')
		clientSock.close()


	def initialiseConnection(self):
		# Send packet 1 (syn packet)

		# 11FalseTrueFalse
		clientPacket = packet.Packet(15200, 8080, 423894, 1, False, True, False, 1024, "hi")
		# clientPacket.setSynBit(True)
		# print(clientPacket.header)
		
		self.clientSend(clientPacket)

		# Receive packet 2

		# Send packet 3

		# Connection established

		# Server sends packet with data

		# Receive packet with data

	def createClient():
		# Set the IP address and port number of the client
		IP = "127.0.0.1"
		port = int(input("Enter your port number: "))

		# Create client instance
		client = Client(IP, port)

		# Start 3 way handshake procedure
		client.initialiseConnection()

# Initialise client with IP and port number
Client.createClient()

	