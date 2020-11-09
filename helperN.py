import socket
import sys
import threading
import time
import errno
from queue import Queue

HEADER_LENGTH=10
all_connections = []
all_address = []
HOST = "localhost"
PORT = 5054
queue = Queue()

username=input("Username:")
username=username+"-helper"
client_socket=socket.socket()
client_socket.connect((HOST,PORT))
client_socket.setblocking(True)

name=username.encode('utf-8')
name_header= f"{len(name):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(name_header+name)
print("Enter list to list available connections:")
connection=True
while connection:
    

        cmd = input()
        if cmd == 'done':
            client_socket.send(str.encode(cmd))
            connection=False
            print("The service has been disconnected.\n")
            break
        if len(str.encode(cmd)) > 0:
            client_socket.send(str.encode(cmd))
            response = str(client_socket.recv(20480), "utf-8")
            print(response, end="")


