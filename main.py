# import server
import client
# import packet
# from client import *

# server = server.Server()
client = client.Client('127.0.0.1', 12500)

client.initialiseConnection()