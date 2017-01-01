#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
from dashing.widgets import NumberWidget, ListWidget
from random import randint

users = randint(50, 100)


class NewClientsWidget(NumberWidget):
    title = 'New Users LOL'

    def get_value(self):
        global users
        users += 1
        return users

    def get_detail(self):
        global users
        return '{} actives'.format(10)

    def get_more_info(self):
        global users
        return '{} fakes'.format(120)


# class ActiveMessengersWidget(ListWidget):
#     title = 'Active Messengers'
#     more_info = 'Those who have more requests'
#
#     def get_updated_at(self):
#         modified = SearchQuerySet().filter(
#             django_ct='errand').order_by('-modified')[0].modified
#         return u'Last updated {}'.format(modified)
#
#     def get_data(self):
#         messengers = SearchQuerySet().filter(
#             django_ct='messengers', active=True)
#         rlist = Counter([x for x in messengers])
#         return [{'label': x, 'value': y} for x, y in rlist.most_common(20)]
