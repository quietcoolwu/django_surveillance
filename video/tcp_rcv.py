#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DESTINATION_ADDR = '192.168.1.126'
TCP_DESTINATION_PORT = 50000


s.connect((DESTINATION_ADDR, TCP_DESTINATION_PORT))
for i in xrange(10):
    data = '07FF'.decode('hex')
    s.send(data)
    time.sleep(1)
    content = s.recv(1024).encode('hex')
    print type(content)
    print 'test'+str(i), content, content is None
    # s.close()
