# DHCP Server

import os
import time
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
expireTime = {}

def server(mac):
    
    if mac in clients.keys():
        print("{} removed {} available to use.".format(mac, clients[mac]))
        
        del clients[mac]
        del expireTime[mac]
        
        return bytes(str("Disconnect : {}".format(mac)), "utf-8")
    addresses = [addr for addr in ipaddress.ip_network('192.168.0.0/24', strict=False) if addr not in clients.values()]

    # give ip address
    clients[mac] = sorted(addresses)[0]
    expireTime[mac] = time.time() + interval 
    
    print("{} served as {}".format(mac, clients[mac]))
    
    return bytes(str(clients[mac]), "utf-8") 

def timer():
    for mac, expire in expireTime.items():
        if time.time() >= expire:
            print("{} expire add 10 sec".format(mac))
            expireTime[mac] += interval

print("DHCP Server Start ...")
while True:  
    
    connection, address = dhcpServer.accept()  
    macAddress = connection.recv(1024)

    timer()
    
    connection.send(server(macAddress.decode("utf-8")))
    connection.close()




