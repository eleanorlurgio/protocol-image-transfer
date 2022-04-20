# import server
import client
# import packet

print("in")
# server = server.Server()
client = client.Client('127.0.0.1', 12500)

print("init")
client.initialiseConnection()