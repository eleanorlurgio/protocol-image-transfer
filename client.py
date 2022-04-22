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
import packet

HEADER_SIZE = 24
DATA_SIZE = 1000000
BUFFER_SIZE = HEADER_SIZE + DATA_SIZE

class Client:

	def __init__(self, sourceIP, sourcePort):
		self.sourceIP = sourceIP
		self.sourcePort = sourcePort

	# The connection is defined by a tuple (source IP, source port, destination IP, destination port)
	# Send data
	def clientSend(self, packetToSend, destinationPort):
		# Create a UDP socket
		UDP_IP_ADDRESS = self.sourceIP
		UDP_PORT_NO = destinationPort

		# Create a socket with a 1s timeout
		clientSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		clientSock.settimeout(2.0)

		while True:
			# Send the message using the clientSock
			# clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
			clientSock.sendto(packetToSend.toByteArray(), (UDP_IP_ADDRESS, UDP_PORT_NO))

			# Receive response
			print('waiting to receive')

			# Get the response & extract data
			try:
				serverPacket = clientSock.recvfrom(BUFFER_SIZE)
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

		sourcePort = int.from_bytes(message[0:2], byteorder='big')
		destPort = int.from_bytes(message[2:4], byteorder='big')
		seqNum = int.from_bytes(message[4:8], byteorder='big')
		ackNum = int.from_bytes(message[8:12], byteorder='big')
		ackBit = int.from_bytes(message[12:16], byteorder='big')
		synBit = int.from_bytes(message[16:20], byteorder='big')
		finBit = int.from_bytes(message[20:24], byteorder='big')
		data = message[24:]

		print("\n* CLIENT HAS RECEIVED *")
		print("Source port: " + str(sourcePort))
		print("Destination port: " + str(destPort))
		print("Sequence number: " + str(seqNum))
		print("Ack number: " + str(ackNum))
		print("Ack bit: " + str(ackBit))
		print("Syn bit: " + str(synBit))
		print("Fin bit: " + str(finBit))
		print("Data: " + str(data))
        # print("Data: " + str(int.from_bytes(message[0:1], byteorder='big')))

		# Check bits of received packet

        # If synBit == 1 and ackBit = 1
		if (synBit == 1) and (ackBit == 1):
			print("Handshake 2/3 complete")

            # sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, windowSize, data
			clientPacket = packet.Packet(self.sourcePort, int.from_bytes(message[0:2], byteorder='big'), int.from_bytes(message[8:12], byteorder='big'), (int.from_bytes(message[4:8], byteorder='big') + 1), True, False, False, 1024, 0)
			self.clientSend(clientPacket, (int.from_bytes(message[0:2], byteorder='big')))


		# Close the socket
		# exit = str(input("Close connection? y/n: "))

		# if exit == 'y':
		print('closing socket')
		clientSock.close()

	# def generatePacket():


	def initialiseConnection(self):
		# Handshake 1/3

		# sourcePort, destinationPort, seqNum, ackNum, ackBit, synBit, finBit, windowSize, data
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

# Initialise client with IP and port number
Client.createClient()

	