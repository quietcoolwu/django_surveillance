#!/usr/bin/env python
#  encoding: utf-8

from __future__ import print_function

import json
import os
import socket
import time

IP_HEAD = '192.168.0.'
DATA_UDP = '064D4243'.decode('hex')
DATA_ENV_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_TARGET_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_TARGET_PORT = 50002, 50000
pardir = os.path.abspath(os.path.join(os.path.dirname('__file__'), os.path.pardir))
DATA_PATH = os.path.join(pardir, r'static/data/')


class Locate(object):
    def __init__(self):
        self.ip = '0'

    def active_writing(self, temperature, humidity, flag):
        # if humidity is not None and temperature is not None:
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = {
            "time": time.strftime('%H:%M', time.localtime(time.time())),
            "tmp": str(temperature),
            "hmt": str(humidity),
            # "plc_data": str(plc_data)
        }
        if not flag:
            self.json_write(data, today, time_scope="min")
        else:
            self.json_write(data, today, time_scope="hour")

    @staticmethod
    def json_write(data, today, time_scope):
        fp = os.path.join(DATA_PATH, time_scope, (today + r'.json'))
        # print(fp)
        if os.path.exists(fp):
            f = open(fp, "rb+")
            f.seek(-1, os.SEEK_END)
            f.truncate()
            f.write(",")
            json.dump(data, f)
            f.write("]")
            f.close()
        else:
            f = open(fp, "w")
            f.write("[")
            json.dump(data, f)
            f.write("]")
            f.close()

    def udp_scan(self):
        self.__init__()
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.settimeout(0.05)
        s_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s_udp.bind(('0.0.0.0', UDP_SOURCE_PORT))
        for i in range(100, 256):
            temp_address = (IP_HEAD + str(i), UDP_TARGET_PORT)
            try:
                s_udp.sendto(DATA_UDP, temp_address)
                target_ip = s_udp.recvfrom(1024)[1][0]
            except socket.error as e:
                print('UDP ERROR!' + str(i), e)
            else:
                self.ip = target_ip
                break

        s_udp.close()
        # time.sleep(0.5)
        return None

    def tcp_scan(self):
        self.udp_scan()
        s_env_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_env_tcp.settimeout(2)
        timer = 0
        try:
            s_env_tcp.connect((self.ip, TCP_TARGET_PORT))
        except socket.error as e:
            print('TCP initial ERROR!Trying to reconnect...', e)
            self.tcp_scan()
        else:
            while True:
                try:
                    s_env_tcp.send(DATA_ENV_TCP)
                    rcv_content = s_env_tcp.recv(1024).encode('hex')
                except socket.error as e:
                    print('TCP MIDWAY ERROR!Trying to reconnect...', e)
                    self.tcp_scan()
                else:
                    # hex to dec
                    temperature = int(rcv_content[2:4], 16)
                    humidity = int(rcv_content[4:6], 16)
                    plc_data = int(rcv_content[6:], 16)
                    print(rcv_content, timer, temperature, humidity, plc_data)
                    self.active_writing(temperature, humidity, flag=timer % 3600 < 5)
                finally:
                    time.sleep(10)
                    timer += 10
                    if timer > pow(2, 30):
                        timer = 0
        return None


if __name__ == '__main__':
    x = Locate()
    x.tcp_scan()
