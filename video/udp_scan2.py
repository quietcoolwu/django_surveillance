# encoding: utf-8


IP_HEAD = '192.168.1.'
import socket, sys

# addr = ('192.168.1.126', 50003)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0', 50004))
data1 = '064D4243'.decode('hex')

for i in xrange(100, 150):
    addr = (IP_HEAD + str(i), 50003)
    s.sendto(data1, addr)
    print 'test1'
    data = s.recvfrom(10)
    s.settimeout(2)
    print 'test2'
    if not data:
        print 'break'
        break
    print data
