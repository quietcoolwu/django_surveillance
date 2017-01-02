#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os
import json
import time
import random

from dashing.widgets import ListWidget, NumberWidget
from settings import BASE_DIR

users = 0
timer = 0

DATA_PATH = os.path.join(BASE_DIR, r'static/data/min/')


class NewClientsWidget(NumberWidget):
    title = 'New Users'

    def get_value(self):
        global users
        users += 1
        return users

    def get_detail(self):
        global users
        return '{} actives'.format(users // 3)

    def get_more_info(self):
        global users
        return '{} fakes'.format(users // 10)


class PLCDataWidget(ListWidget):
    title = 'PLC 数据监控表'
    more_info = 'PLC 数据的实时监控'

    def get_data(self):
        global timer
        plc_monitoring_parameters = {'speed': timer, 'loc': timer * 2}
        timer += 1
        print(timer, plc_monitoring_parameters, DATA_PATH)
        return [{'label': x, 'value': y} for x, y in plc_monitoring_parameters.items()]
