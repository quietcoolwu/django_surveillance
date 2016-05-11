import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

DESTINATION_ADDR = '192.168.1.126'
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0', UDP_SOURCE_PORT))

for i in xrange(10):
    data = '064D4243'.decode('hex')
    s.sendto(data, (DESTINATION_ADDR, UDP_DESTINATION_PORT))
    print 3
    content = s.recv(1024).encode('hex')
    print 4
    time.sleep(1)
    print 'test' + str(i), content
    # s.close()
