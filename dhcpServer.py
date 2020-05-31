








# DHCP Server

import os
import socket
import ipaddress

HOST, PORT = "localhost", 9999

# in secs
interval = 10

dhcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
dhcpServer.bind((HOST, PORT))  

# the max number of connection that made at the same time
# see max value vim  /proc/sys/net/core/somaxconn
dhcpServer.listen(128)

# all clients addresses range is 192.168.0.0 -> 192.168.0.255
clients = {}

def server(mac):
    
    if mac in clients.keys():
        del clients[mac]
        return bytes(str("Disconnect : {}".format(mac)), "utf-8")
    addresses = [addr for addr in ipaddress.ip_network('192.168.0.0/24', strict=False) if addr not in clients.values()]

    # give ip address
    clients[mac] = sorted(addresses)[0]
    return bytes(str(clients[mac]), "utf-8") 

while True:  
    connection, address = dhcpServer.accept()  
    buf = connection.recv(1024)
    print(connection, address)
    connection.send(server(buf))
    print(buf)
    connection.close()




