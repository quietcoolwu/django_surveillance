#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
from dashing.widgets import NumberWidget
from random import randint

users = randint(50, 100)
print('haha', users)


class NewClientsWidget(NumberWidget):
    title = 'New Users LOL'
    print(users)

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
