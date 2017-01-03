#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import json
import os
import random
import time

from dashing.widgets import ListWidget, NumberWidget

from settings import BASE_DIR

users = random.randint(50, 100)
timer = 0
DATA_MIN_PATH = os.path.join(BASE_DIR, r'static/data/min/')
EN_CN_MAPPING = {'tmp': r'温度(C)',
                 'gun_speed': r'枪架速度(mm/s)',
                 'hmt': '湿度(%)',
                 'gun_location': r'枪架位置(mm)',
                 'time': r'时刻',
                 'input_material_speed': r'送料速度(m/min)'}


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
    more_info = 'PLC 数据实时监控'

    def get_data(self):
        global timer
        timer += 1
        # test_flag
        test_flag = True
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log_path = os.path.join(DATA_MIN_PATH, today + r'.json')
        res = dict((label, random.randint(10, 100))
                   for label in EN_CN_MAPPING.values())

        if os.path.exists(log_path):
            if not test_flag:
                with open(log_path, 'r') as f:
                    plc_json = json.load(f)
                if plc_json:
                    for en_name, cn_name in EN_CN_MAPPING.items():
                        res[cn_name] = plc_json[-1].pop(en_name)

        # print(res, log_path)
        return [{'label': x, 'value': y} for x, y in res.items()]
