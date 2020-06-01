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

# all clientsTable addresses range is 192.168.0.0 -> 192.168.0.255
clientsTable = {}
expireTime = {}

def server(mac):
    
    if mac in clientsTable.keys():
        print("{} removed {} available to use.".format(mac, clientsTable[mac]))
        
        del clientsTable[mac]
        del expireTime[mac]

        updateTable()
        
        return bytes(str("Disconnect : {}".format(mac)), "utf-8")
    addresses = [addr for addr in ipaddress.ip_network('192.168.0.0/24', strict=False) if addr not in clientsTable.values()]

    # give ip address
    clientsTable[mac] = sorted(addresses)[0]
    expireTime[mac] = time.time() + interval 
    
    print("{} served as {}".format(mac, clientsTable[mac]))
    
    return bytes(str(clientsTable[mac]), "utf-8") 

def updateTable():

    for i, j in enumerate(clientsTable.items()):
       clientsTable[j[0]] = ipaddress.ip_address('192.168.0.0') + i

def timer():

    for mac, expire in expireTime.items():
        if time.time() >= expire:
            updateTable()
            print("{} expire add 10 sec".format(mac))
            expireTime[mac] += interval

print("DHCP Server Start ...")
while True:  
    
    connection, address = dhcpServer.accept()  
    macAddress = connection.recv(1024)

    timer()
    
    connection.send(server(macAddress.decode("utf-8")))
    connection.close()

