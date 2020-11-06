import socket
import select
from queue import Queue 

HEADER_LENGTH=10
all_connections = []
all_address = []
HOST = "localhost"
PORT = 5054
queue = Queue()

server_socket = socket.socket()
server_socket.bind((HOST,PORT))

server_socket.listen()

sockets_list=[server_socket]
clients={}


def received_code(client_socket):
    try:
        message_header=client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length=int(message_header.decode('utf-8').strip())
        return {"header": message_header,"data": client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_sockets=select.select(sockets_list,[],sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket,client_address=server_socket.accept()

            user=received_code(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket]=user

            print(f"Accepted new connection form {client_address[0]}:{client_address[1]} username {user['data'].decode('utf-8')}")

        else:
            message=notified_socket.recv(2048)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            #print(f"Received message from {user['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(message)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
