import socket
import time

IP_HEAD = '192.168.1.'
UDP_DATA_MAC = '064D4243'.decode('hex')
TCP_DATA_ENV = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_DESTINATION_PORT = 50002, 50000

s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))

for i in xrange(100, 200):
    link = IP_HEAD + str(i)
    print 'test' + str(i)
    s_tcp.settimeout(8)
    try:
        s_tcp.connect_ex((link, TCP_DESTINATION_PORT))
    except socket.error as e:
        print 'socket error', link, e
        continue
    else:
        #s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))
        s_udp.sendto(UDP_DATA_MAC, (link, UDP_DESTINATION_PORT))
        rcv_content = s_udp.recv(30).encode('hex')
        print rcv_content





        # print link
        # rcv_content = s_udp.recv(30).encode('hex')
        # if not rcv_content:
        #     print 'fail'
        #     i += 1
        # else:
        #     print 'test' + str(i), rcv_content
