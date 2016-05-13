# encoding: utf-8

import socket
import time

IP_HEAD = '192.168.1.'
DATA_UDP = '064D4243'.decode('hex')
DATA_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_DESTINATION_PORT = 50002, 50000


def ip_scan():
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_udp.settimeout(0.015)
    s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))
    target_ip = 0
    for i in xrange(100, 150):
        addr = (IP_HEAD + str(i), UDP_DESTINATION_PORT)
        try:
            s_udp.sendto(DATA_UDP, addr)
            target_ip = s_udp.recvfrom(1024)[1][0]
        except socket.timeout as e:
            print 'udp_timeout!' + str(i), e
        except socket.error as e:
            print 'udp lose connection', e
        else:
            print target_ip
            break

    s_udp.close()

    if target_ip:
        s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tcp.settimeout(3)
        try:
            s_tcp.connect((target_ip, TCP_DESTINATION_PORT))
        except socket.error as e:
            print 'tcp lose connection!', e
            return None
        else:
            while True:
                try:
                    s_tcp.send(DATA_TCP)
                    content = s_tcp.recv(1024).encode('hex')
                except socket.timeout as e:
                    print 'tcp_timeout', e
                    time.sleep(2)
                else:
                    print 'content', content, type(content)
                    time.sleep(1)
            return target_ip
    else:
        return None


if __name__ == '__main__':
    ip_scan()
