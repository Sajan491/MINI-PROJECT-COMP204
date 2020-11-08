import socket
import os
import subprocess

HOST = "localhost"
PORT = 5054


username=input("Username:")
username=username+'-client'
s=socket.socket()
s.connect((HOST,PORT))

name=username.encode('utf-8')
name_header= f"{len(name):<{10}}".encode('utf-8')
s.send(name_header+name)
connected = True
while connected:
    data = s.recv(1024)
    if data[:8].decode("utf-8") == 'workdone':
        connected = False
        s.send(str.encode("The connection has been terminated."+"\n"))
        print("The connection has been terminated.")
        break

    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode(
            "utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))

        data1 = data.decode("utf-8")
        print(f"{currentWD}{data1}")
        print(output_str)

