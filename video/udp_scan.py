#!usr/bin/env python
import socket

host = '0.0.0.0'
port = 50004
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
while True:
    try:
        data, addr = s.recvfrom(1024)
        print "got data from", addr
        s.sendto("broadcasting", addr)
        print data
    except KeyboardInterrupt:
        raise
