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
        temp_address = (IP_HEAD + str(i), UDP_DESTINATION_PORT)
        try:
            s_udp.sendto(DATA_UDP, temp_address)
            target_ip = s_udp.recvfrom(1024)[1][0]
        except socket.error as e:
            print 'udp error!' + str(i), e
        else:
            print target_ip
            break

    s_udp.close()

    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.settimeout(3)

    try:
        s_tcp.connect((target_ip, TCP_DESTINATION_PORT))
    except socket.error as e:
        print 'tcp error!', e
    else:
        while True:
            try:
                s_tcp.send(DATA_TCP)
                content = s_tcp.recv(1024).encode('hex')
                print 'content', content, type(content)
            except socket.error as e:
                print 'midway error!', e
            finally:
                time.sleep(1)
    

if __name__ == '__main__':
    ip_scan()
