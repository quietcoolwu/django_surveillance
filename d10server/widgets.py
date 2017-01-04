#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os
import random
import time
from collections import OrderedDict

from dashing.widgets import ListWidget, NumberWidget

from .settings import BASE_DIR

JSON_MIN_DIR = os.path.join(BASE_DIR, r'static/data/min/')
EN_CN_MAPPING = OrderedDict({'time': r'时刻',
                             'tmp': r'温度(C)',
                             'hmt': r'湿度(%)',
                             'gun_speed': r'枪架速度(mm/s)',
                             'gun_location': r'枪架位置(mm)',
                             'input_material_speed': r'送料速度(m/min)'})


class NewClientsWidget(NumberWidget):
    title = '当前监控车床编号'

    def get_value(self):
        return '{}'.format(random.randint(10, 100))

    def get_detail(self):
        return '{} 个枪架工作中'.format(random.randint(10, 100))


class PLCDataWidget(ListWidget):
    title = '智能数据监控板'
    more_info = 'PLC 数据实时监控'

    def get_data(self):
        # on_prod: True in production line
        on_prod = False
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        json_path = os.path.join(JSON_MIN_DIR, today + r'.json')
        res = dict((label, random.randint(10, 100))
                   for label in EN_CN_MAPPING.values())

        if on_prod:
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    plc_json = json.load(f)
                if plc_json:
                    for en_name, cn_name in EN_CN_MAPPING.items():
                        res[cn_name] = plc_json[-1].pop(en_name)

        # print(res, json_path)
        return [{'label': x, 'value': y} for x, y in res.items()]
