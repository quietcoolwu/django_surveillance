# encoding: utf-8

import socket
import time

IP_HEAD = '192.168.1.'
DATA_UDP = '064D4243'.decode('hex')
DATA_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_DESTINATION_PORT = 50002, 50000


class Locate(object):
    def __init__(self, ip):
        self.ip = ip

    def udp_scan(self):
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.settimeout(0.02)
        s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))
        for i in xrange(100, 150):
            temp_address = (IP_HEAD + str(i), UDP_DESTINATION_PORT)
            try:
                s_udp.sendto(DATA_UDP, temp_address)
                target_ip = s_udp.recvfrom(1024)[1][0]
            except socket.error as e:
                print 'UDP ERROR!' + str(i)
            else:
                self.ip = target_ip
                break

        s_udp.close()
        print 'target_ip is ', self.ip

    def tcp_scan(self):
        self.udp_scan()
        s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tcp.settimeout(2)
        try:
            s_tcp.connect((self.ip, TCP_DESTINATION_PORT))
        except socket.error as e:
            print 'TCP initial ERROR!Trying to reconnect...', e
            self.tcp_scan()
        else:
            while True:
                try:
                    s_tcp.send(DATA_TCP)
                    content = s_tcp.recv(1024).encode('hex')
                    print 'content', content, type(content)
                except socket.error as e:
                    print 'TCP MIDWAY ERROR!Trying to reconnect...', e
                    self.tcp_scan()
                finally:
                    time.sleep(1)


if __name__ == '__main__':
    x = Locate('0')
    x.tcp_scan()
