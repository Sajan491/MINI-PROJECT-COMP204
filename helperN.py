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
client_socket=socket.socket()
client_socket.connect((HOST,PORT))
client_socket.setblocking(True)

name=username.encode('utf-8')
name_header= f"{len(name):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(name_header+name)

while True:
    # message=input(f"{username} >")

    # if message:
    #     message = message.encode('utf-8')
    #     message_header=f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    #     client_socket.send(message_header + message)
    
    # try:
    #     while True:
    #         name_header=client_socket.recv(HEADER_LENGTH)
    #         if not len(name_header):
    #             print("Connection closed by the server")
    #             sys.exit()
    #         username_length=int(name_header.decode('utf-8').strip())
    #         name=client_socket.recv(HEADER_LENGTH)

    #         message_header=client_socket.recv(HEADER_LENGTH)
    #         message_length=int(message_header.decode('utf-8').strip())
    #         message=client_socket.recv(message_length).decode('utf-8')

    #         print(f"{username}>{message}")


    # except IOError as e:
    #     if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
    #         print('Reading error',str(e))
    #     continue
    
    # except Exception as e:
    #     print('General error',str(e))
    #     sys.exit()
        cmd = input()
        if cmd == 'workdone':
            client_socket.send(str.encode(cmd))
            client_socket.close()
            break
        if cmd == 'quitclient':
            break
        if len(str.encode(cmd)) > 0:
            client_socket.send(str.encode(cmd))
            print('sent')
            response = str(client_socket.recv(20480), "utf-8")
            print(response, end="")
