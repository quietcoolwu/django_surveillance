#!/usr/bin/env python
#  encoding: utf-8

import sys
import time
import json
import os
import string


def json_read(source, target, name):
    s_path = source + '/' + name
    t_path = target + '/' + name
    if os.path.exists(s_path):
        f = open(s_path, "r")
        data = json.loads(f.read().decode('utf-8'))
        i = 1
        json_write(data[0], t_path)
        for v in data:
            i += 1
            if i % 60 == 0:
                json_write(v, t_path)
        f.close()
    else:
        print 'unable to open ' + s_path + 'file'


def json_write(data, t_path):
    if os.path.exists(t_path):
        f = open(t_path, "rb+")
        f.seek(-1, os.SEEK_END)
        f.truncate()
        f.write(",")
        json.dump(data, f)
        f.write("]")
        f.close()
        print 'success: ' + t_path
    else:
        f = open(t_path, "w")
        f.write("[")
        json.dump(data, f)
        f.write("]")
        f.close()


dir = '../static/data/min'
dist = '../static/data/hour'
files = os.listdir(dir)

for root, dirs, files in os.walk(dir):
    for name in files:
        json_read(dir, dist, name)
