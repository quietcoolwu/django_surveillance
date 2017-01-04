#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals

import json
import os
import time
from datetime import datetime

import unicodecsv as csv
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from d10server.settings import BASE_DIR
from d10server.widgets import JSON_MIN_DIR, EN_CN_MAPPING
from video.models import Article

SHEETS_DIR = os.path.join(BASE_DIR, r'static/data/sheets/')


# Create your views here.
def home(request):
    post_list = Article.objects.all()
    return render(request, 'home.html', {'post_list': post_list})


def test(request):
    return render(request, 'test.html', {'current_time': datetime.now()})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))

    except Article.DoesNotExist:
        raise Http404

    return render(request, 'post.html', {'post': post})


def video(request):
    return render(request, 'video.html')


def env(request):
    return render(request, 'env.html')


def prod_index(request):
    return render(request, 'prod_index.html')


def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(today)
    print(response, type(response))

    json_path = os.path.join(JSON_MIN_DIR, today + r'.json')

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            plc_json = json.load(f)
        if plc_json:
            writer = csv.writer(response, encoding='gbk')
            writer.writerow(EN_CN_MAPPING.values())
            for data in plc_json:
                # print(data)
                writing_res = list()
                for en_name in EN_CN_MAPPING.keys():
                    writing_res.append(data.get(en_name, '数据不存在'))
                writer.writerow(writing_res)

            return response
