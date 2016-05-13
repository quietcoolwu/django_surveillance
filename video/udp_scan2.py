# encoding: utf-8

import socket
import time

IP_HEAD = '192.168.1.'
DATA_UDP = '064D4243'.decode('hex')
DATA_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_DESTINATION_PORT = 50002, 50000


def udp_scan():
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_udp.settimeout(0.01)
    s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))

    for i in xrange(100, 150):
        addr = (IP_HEAD + str(i), UDP_DESTINATION_PORT)
        s_udp.sendto(DATA_UDP, addr)
        print 'test1'
        try:
            udp_rcv_content = s_udp.recvfrom(1024)[1][0]
            print 'test' + str(i), udp_rcv_content, type(udp_rcv_content)
        except socket.timeout as e:
            print 'test' + str(i), 'fail'
            continue

    s_udp.close()


# time.sleep(1)

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'here', udp_rcv_content
s_tcp.connect((udp_rcv_content, TCP_DESTINATION_PORT))
s_tcp.send(DATA_TCP)
content = s_tcp.recv(1024).encode('hex')
print type(content)
print content, content is None
