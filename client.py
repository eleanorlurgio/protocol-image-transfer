# import server
from asyncio.windows_events import NULL
import random
from socket import *
from email import message
import sys
from threading import Thread
import socket
from time import sleep, time
from cv2 import cv2
import numpy
import packet

HEADER_SIZE = 24
DATA_SIZE = 600
BUFFER_SIZE = HEADER_SIZE + DATA_SIZE

img = []

sys.setrecursionlimit(15000)

class Client:

	def __init__(self, sourceIP, sourcePort):
		self.sourceIP = sourceIP
		self.sourcePort = sourcePort
		self.closing = False

	# Client listens and responds
	def clientSend(self, packetToSend, destinationPort):
		# Define IP address and port number to send to (both client and server on the same IP address)
		UDP_IP_ADDRESS = self.sourceIP
		UDP_PORT_NO = destinationPort

		# Create a UDP socket with a timeout of 1.0 second
		clientSock = socket.socket(family=AF_INET, type=SOCK_DGRAM)
		clientSock.settimeout(1.0)

		# Send packet as bytearray

		# Client listens continuously
		while True:
			while True:
				try:
					clientSock.sendto(packetToSend.toByteArray(), (UDP_IP_ADDRESS, UDP_PORT_NO))
				except ConnectionResetError:
					print("Server not up")
					sleep(0.1)
					continue
				break

			# Receive packet from clientSock, show error message if nothing is received and continue listening
			try:
				serverPacket = clientSock.recvfrom(BUFFER_SIZE)
			except TimeoutError:
				print("Timeout")
				sleep(0.1)
				continue
			except ConnectionResetError:
				print("Server not up")
				sleep(0.1)
				continue
			break

		# Split received packet into contents and address
		message = serverPacket[0]
		address = serverPacket[1]

		# Read bytes
		sourcePort = int.from_bytes(message[0:2], byteorder='big')
		destPort = int.from_bytes(message[2:4], byteorder='big')
		seqNum = int.from_bytes(message[4:8], byteorder='big')
		ackNum = int.from_bytes(message[8:12], byteorder='big')
		ackBit = int.from_bytes(message[12:16], byteorder='big')
		synBit = int.from_bytes(message[16:20], byteorder='big')
		finBit = int.from_bytes(message[20:24], byteorder='big')
		data = message[24:]

		# Display packet contents in terminal
		print("\n* CLIENT HAS RECEIVED *")
		print("Source port: " + str(sourcePort))
		print("Destination port: " + str(destPort))
		print("Sequence number: " + str(seqNum))
		print("Ack number: " + str(ackNum))
		print("Ack bit: " + str(ackBit))
		print("Syn bit: " + str(synBit))
		print("Fin bit: " + str(finBit))
		print("Data: " + str(data))

		# Check bits of received packet to respond accordingly

        # Complete handshake 2/3
		if (synBit == 1) and (ackBit == 1):
			print("Opening handshake 2/3 complete")

            # Send response packet
			clientPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[8:12], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, False, 1024, NULL)
			self.clientSend(clientPacket, (int.from_bytes(message[0:2], byteorder='big')))

		# RECEIVE IMAGE

		# Check if there is an image received
		if data:
			# print("data received")

			img.append(data)

			ackPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[24:25], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, False, 1024, NULL)
			self.clientSend(ackPacket, (int.from_bytes(message[0:2], byteorder='big')))


		if (finBit == 1) and (self.closing == False):
			self.closing = True
			print("Closing handshake 1/4 complete")

			fullImg = b''
			for i in range(-1, len(img)):
				fullImg = fullImg + img[i]
				i += 1

			# Decodes data into a 1D array
			decoded = numpy.frombuffer(fullImg, dtype=numpy.uint8)
			# # Reshapes the image to its original formation
			decoded = decoded.reshape((360, 360, 3))
			# # Displays image in a window until closed
			cv2.imshow('Image', decoded)
			cv2.waitKey(0)

			self.endConnection(message, clientSock, UDP_IP_ADDRESS, UDP_PORT_NO)


		if (finBit == 1) and (self.closing == True):
			print("Closing handshake 4/4 complete")
			
		
		# Close socket and terminate
		clientSock.close()

	def endConnection(self, message, clientSock, UDP_IP_ADDRESS, UDP_PORT_NO):
			# Close connection 2/4
			closePacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[24:25], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, False, 1024, NULL)
			# self.clientSend(closePacket, (int.from_bytes(message[0:2], byteorder='big')))
			clientSock.sendto(closePacket.toByteArray(), (UDP_IP_ADDRESS, UDP_PORT_NO))
			
			# Close connection 3/4
			closePacket2 = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[24:25], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, True, 1024, NULL)
			self.clientSend(closePacket2, (int.from_bytes(message[0:2], byteorder='big')))

	def initialiseConnection(self):
		# Create and send first packet
		clientPacket = packet.Packet(self.sourcePort, 8080, random.randint(0, 2147483647), 0, False, True, False, 1024, NULL)
		
		self.clientSend(clientPacket, 8080)


	def createClient():
		# Set the IP address and port number of the client
		IP = "127.0.0.1"
		port = int(input("Enter your port number: "))

		# Create client instance
		client = Client(IP, port)

		# Start 3 way handshake procedure
		client.initialiseConnection()

# Initialise client
Client.createClient()

	