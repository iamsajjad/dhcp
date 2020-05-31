# DHCP Client

import sys
import socket
import random

def macGen():
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))

HOST, PORT = "localhost", 9999
Dmac = " ".join([macGen()])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    

    try: 
        if sys.argv[1] == "--kill":
            sock.sendall(bytes(sys.argv[2], "utf-8"))
            print("Disconnect :   {}".format(sys.argv[2]))
    except:
            sock.sendall(bytes(Dmac, "utf-8"))
            print("Device Mac Address:   {}".format(Dmac))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("DHCP Server Respones: {}".format(received))
