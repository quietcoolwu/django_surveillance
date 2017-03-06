#!/usr/bin/env python
#  encoding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os
import re
import socket
import time

from d10server.settings import BASE_DIR

IP_HEAD = '192.168.0.'
DATA_UDP = '064D4243'.decode('hex')
DATA_ENV_TCP = '07FF'.decode('hex')
UDP_SOURCE_PORT, UDP_TARGET_PORT = 50004, 50003
TCP_SOURCE_PORT, TCP_TARGET_PORT = 50002, 50000
DATA_PATH = os.path.join(BASE_DIR, r'static/data/')


class Locate(object):
    def __init__(self):
        self.ip = '0'

    def periodical_writing(self, temperature, humidity, plc_data, flag):
        # if humidity is not None and temperature is not None:
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = {
            "time": time.strftime('%H:%M', time.localtime(time.time())),
            "tmp": str(temperature),
            "hmt": str(humidity),
            "input_material_speed": str(plc_data[0] / 10),  # m/min
            "gun_speed": str(plc_data[1]),  # mm/s
            "gun_location": str(plc_data[3] / 100),  # mm
        }
        print(data, DATA_PATH)
        if not flag:
            self.json_write(data, today, time_scope="min")
        else:
            self.json_write(data, today, time_scope="hour")

    @staticmethod
    def json_write(data, today, time_scope):
        log_path = os.path.join(DATA_PATH, time_scope, (today + r'.json'))
        if os.path.exists(log_path):
            out = open(log_path, 'rb+')
            out.seek(-1, os.SEEK_END)
            out.truncate()
            out.write(str(','))
            json.dump(data, out, sort_keys=True, indent=4, encoding='utf-8', ensure_ascii=False)
            out.write(str(']'))
            out.close()
        else:
            out = open(log_path, 'w')
            out.write(str('['))
            json.dump(data, out, sort_keys=True, indent=4, encoding='utf-8', ensure_ascii=False)
            out.write(str(']'))
            out.close()

    def udp_scan(self):
        self.__init__()
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.settimeout(0.2)
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
        time.sleep(0.5)
        return None

    def tcp_connect(self):
        self.udp_scan()
        s_env_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_env_tcp.settimeout(8)
        timer = 0
        try:
            s_env_tcp.connect((self.ip, TCP_TARGET_PORT))
        except socket.error as e:
            print('TCP initial ERROR!Trying to reconnect...', e)
            self.tcp_connect()
        else:
            while True:
                try:
                    s_env_tcp.send(DATA_ENV_TCP)
                    rcv_all_hex = s_env_tcp.recv(1024).encode('hex')
                    # temperature and humidity from MCU
                    on_board_sensor = rcv_all_hex[:6]
                    # only hex2char: data from plc
                    plc_data_hex = rcv_all_hex[6:].decode('hex')
                    # plc_data_hex like: 15000000080700000000000085D30200
                    assert len(plc_data_hex) == 32
                    # slice plc_data_hex
                    plc_hex_slice = re.findall(r'.{8}', plc_data_hex)
                    plc_data = self.plc_data_convert(plc_hex_slice)
                except socket.error as e:
                    print('TCP MIDWAY ERROR!Trying to reconnect...', e)
                    self.tcp_connect()
                else:
                    # hex to dec
                    temperature = int(on_board_sensor[2:4], 16)
                    humidity = int(on_board_sensor[4:], 16)
                    # print(on_board_sensor, timer, temperature, humidity, plc_data)
                    self.periodical_writing(temperature, humidity, plc_data, flag=timer % 3600 < 5)
                finally:
                    time.sleep(10)
                    timer += 10
                    if timer > pow(2, 30):
                        timer = 0

        return self.ip

    def plc_data_convert(self, plc_hex_slice):
        plc_data = list()
        for each in plc_hex_slice:
            # split and reverse high and low digits
            sub_slice = re.findall(r'.{2}', each)
            pre_hex = ''.join(sub_slice[::-1])
            raw_data = int(pre_hex, base=16)
            # if raw_data > 20000:
            #     raw_data -= pow(2, 32)
            plc_data.append(self.int32_overflow(raw_data))
        return plc_data

    @staticmethod
    def int32_overflow(val):
        maxint = pow(2, 31) - 1
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val


if __name__ == '__main__':
    x = Locate()
    x.tcp_connect()
