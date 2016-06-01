# encoding: utf-8

import socket
import time
import json

IP_HEAD = '192.168.1.'
# DATA_UDP = bytes.fromhex('064D4243').decode('utf-8')
DATA_UDP = '064D4243'.decode('hex')
# DATA_TCP = '\x07\xff'
DATA_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_DESTINATION_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_DESTINATION_PORT = 50002, 50000


class Locate(object):
    def __init__(self):
        self.data_json = {'ERROR': 'ERROR'}

    def udp_scan(self):
        self.ip = '0'
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.settimeout(0.04)
        s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))
        for i in range(100, 150):
            temp_address = (IP_HEAD + str(i), UDP_DESTINATION_PORT)
            try:
                s_udp.sendto(DATA_UDP, temp_address)
                target_ip = s_udp.recvfrom(1024)[1][0]
            except socket.error as e:
                print('UDP ERROR!' + str(i), e)
            else:
                self.ip = target_ip
                break

        s_udp.close()
        time.sleep(1)
        # print 'target_ip is ', self.ip

    def tcp_scan(self):
        self.udp_scan()
        s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tcp.settimeout(2)
        try:
            s_tcp.connect((self.ip, TCP_DESTINATION_PORT))
            content_list = []
        except socket.error as e:
            print('TCP initial ERROR!Trying to reconnect...', e)
            self.tcp_scan()
        else:
            while True:
                try:
                    s_tcp.send(DATA_TCP)
                    rcv_content = s_tcp.recv(1024).encode('hex')
                except socket.error as e:
                    print('TCP MIDWAY ERROR!Trying to reconnect...', e)
                    self.tcp_scan()
                else:
                    content_list.append(rcv_content)
                    if len(content_list) > 20:
                        content_list = [content_list[-1]]
                    # self.content = content_list
                    templist = content_list[-1]
                    # if len(templist) == 6:
                    temperature = int(templist[2:4], 16)
                    moisture = int(templist[-2:], 16)
                    final_data = {'temperature': temperature, 'moisture': moisture}
                    self.data_json = json.dumps(final_data, indent=4)
                    print(self.data_json)
                    with open('./data.json', 'w') as f:
                        f.write(self.data_json)
                finally:
                    time.sleep(1)


if __name__ == '__main__':
    x = Locate()
    x.tcp_scan()
