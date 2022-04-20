from server import *
import server
import packet

class Client:

	def __init__(self, sourceIP, sourcePort):
		self.sourceIP = sourceIP
		self.sourcePort = sourcePort

	# The connection is defined by a tuple (source IP, source port, destination IP, destination port)
	# Send data
	def clientSend(self, packet):
		# Create a UDP socket
		UDP_IP_ADDRESS = self.sourceIP
		UDP_PORT_NO = packet.destinationPort

		# Request message from user client
		# Message = str.encode("request photo")

		# Read image
		my_img = cv2.imread("image_black.png", cv2.IMREAD_GRAYSCALE)
		# packet.setData(my_img)
		# print(my_img)
		# cv2.imshow('My image', my_img)
		# cv2.waitKey(0)

		# sleep(1000)

		# Create a socket with a 1s timeout
		clientSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		clientSock.settimeout(1.0)

		# Send data to client
		# print('Ping %d %s' % (1,Message.decode()))

		while True:
			# Send the message using the clientSock
			# clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
			clientSock.sendto(packet.toByteArray(), (UDP_IP_ADDRESS, UDP_PORT_NO))

			# Receive response
			print('waiting to receive')

			# Get the response & extract data
			try:
				data = clientSock.recvfrom(BUFFER_SIZE)
			except TimeoutError:
				print("timeout")
				sleep(0.1)
				continue
			except ConnectionResetError:
				print("server not up")
				sleep(0.1)
				continue
			break

		img = data[0]
		address = data[1]
		print('client received: ' + str(img))

		# Close the socket
		print('closing socket')
		clientSock.close()


	def initialiseConnection(self):
		# Send packet 1
		clientPacket = packet.Packet(self.sourcePort, 12501, 0, 0, 0, 0, 0, "hi")
		# print(clientPacket.header)

		self.clientSend(clientPacket)

		# Receive packet 2

		# Send packet 3

		# Connection established

		# Server sends packet with data

		# Receive packet with data

	# if __name__ == '__main__':
	# 	username = str(input("Enter your username: "))
	# 	# Set IP address to local IP address
	# 	# ip = socket.gethostbyname(socket.gethostname())
	# 	print(socket.gethostbyname(socket.gethostname()))
	# 	source_IP = "0.0.0.0" #socket.gethostbyname(socket.gethostname())
	# 	source_port = 12500
	# 	destination_IP = "localhost" #socket.gethostbyname(socket.gethostname())
	# 	destination_port = 12501
	# 	# port = int(input("Connect to which port number: "))
	# 	# Thread(target = OpenConnection, args=(source_IP, source_port, destination_IP, destination_port)).start()
	# 	OpenConnection(username, source_IP, source_port, destination_IP, destination_port)
	# 	# Thread(target = OpenConnection, args=(client1_IP, client1_port, client2_IP, client2_port)).start()