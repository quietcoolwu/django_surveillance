#!/usr/bin/env python
#  encoding: utf-8

import sys
import Adafruit_DHT
import time
import json, os


def jsonWrite(data, tdate, name):
    fp = "web/data/" + name + "/" + tdate + ".json"
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


while True:
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 26)
    if humidity is not None and temperature is not None:
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        msg = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())) + '\n' + str(temperature) + ' C  ' + str(
            humidity) + '%'
        i = {"time": time.strftime('%H:%M', time.localtime(time.time())), "tmp": temperature, "hmt": humidity}
        jsonWrite(i, today, "min")
        print(msg)
    if (timecount >= 60):
        timecount = 0
        jsonWrite(i, today, "hour")
    time.sleep(60)
    timecount += 1
