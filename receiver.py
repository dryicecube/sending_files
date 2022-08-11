#forcefully kill the port for" 
#sudo lsof -i:5001
#kill -9 12654

####################################33
#IP config = "curl ifconfig.me"


import socket
from tkinter import SEPARATOR
import tqdm
import os
#device ip address

Server_host = "127.0.0.1"
Server_port = 8011

BUFFER_SIZE=4096
SEPARATOR="<SEPARATOR>"

s=socket.socket()
#s.close()
s.bind((Server_host, Server_port))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {Server_host}:{Server_port}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        #progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
