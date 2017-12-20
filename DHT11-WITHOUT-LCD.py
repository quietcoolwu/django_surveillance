#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import os
import sys
import time

import Adafruit_DHT
from d10server.settings import BASE_DIR


def jsonWrite(data, tdate, time_scope):
    # pathfile = "web/data/" + time_scope + "/" + tdate + ".json"
    filepath = os.path.join(BASE_DIR, r'static/data/', time_scope,
                            tdate + ".json")
    if os.path.exists(filepath):
        file = open(filepath, "rb+")
        file.seek(-1, os.SEEK_END)
        file.truncate()
        file.write(",")
        json.dump(data, file)
        file.write("]")
        file.close()
    else:
        file = open(filepath, "w")
        file.write("[")
        json.dump(data, file)
        file.write("]")
        file.close()


min_count = 0
while True:
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 26)
    if humidity and temperature:
        todaytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        msg = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time(
        ))) + '\n' + str(temperature) + ' C  ' + str(humidity) + '%'
        i = {
            "time": time.strftime('%H:%M', time.localtime(time.time())),
            "tmp": temperature,
            "hmt": humidity
        }
        jsonWrite(i, todaytime, "min")
        print(msg)
        # Acc 60 min, write hour data.
        if (min_count >= 60):
            min_count = 0
            jsonWrite(i, todaytime, "hour")
        time.sleep(60)
        min_count += 1
