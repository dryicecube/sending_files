#File transfer of TDC over internet

import socket
from tkinter import SEPARATOR
import tqdm
import os
import time

SEPARATOR ="<SEPARATOR>"
BUFFER_SIZE=4096

host = "127.0.0.1"
port = 8011

filename= "Trial/file.mp4.aes"
filesize = os.path.getsize(filename)


#create client socket

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print("[+] Connected.")
one=time.time()
#send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
time.sleep(2)
# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        #progress.update(len(bytes_read))
# close the socket
s.close()
two=time.time()
print("Time taken to send -", int(two-one), "seconds")
