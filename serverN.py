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

# Accepting Client Connections
def accept_client_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            connection, address = server_socket.accept()
            server_socket.setblocking(1)  # prevents timeout
            all_connections.append(connection)
            all_address.append(address)
            print(
                f"Connection has been established with : {address[0]} at the port {address[1]}")
            print("Enter 'list' to show all available connections.")
            cmd = input("You>")
            if cmd == 'list':
                list_connections()

        except:
            print("Error creating connections")

#To list the connected clients/helpers
def list_connections():
    results = ''
    try:
        for i, c in enumerate(all_connections):
            c.send(str.encode(' '))
            c.recv(2048)
            results = str(
                i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

        print(f"----Available Connections---- + '\n' {results}")
    except:
        print("No connections available")

def received_code(client_socket):
    try:
        message_header=client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length=int(message_header.decode('utf-8').strip())
        return {"header": message_header,"data": client_socket.recv(message_length)}

    except:
        return False

print(f"Server successfully started at the port {PORT}. \n Accepting new connections.......")


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

            print(f"Accepted new connection form {client_address[0]}:{client_address[1]} with Username {user['data'].decode('utf-8')}")


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

def start():
    active = True
    while active:
        global s
        cmd = input("You>")
        if cmd == 'closeserver':
            for c in all_connections:
                c.send(str.encode('workdone'))
        elif cmd == 'list':
            list_connections()
        else:
            print("Enter 'list' to list all connections availabele.")

start();