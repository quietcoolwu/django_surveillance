#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import json
import os
import time
from datetime import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render

import unicodecsv as csv
from d10server.widgets import EN_CN_MAPPING, JSON_MIN_DIR
from video.models import Article


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


def p2p_video(request):
    return render(request, 'p2p_video.html')


def env(request):
    return render(request, 'env.html')


def prod_index(request):
    return render(request, 'prod_index.html')


def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(
        today)

    json_path = os.path.join(JSON_MIN_DIR, today + r'.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            plc_json = json.load(f)
        if plc_json:
            # Must encoding as gbk for Windows Excel compatibility
            writer = csv.writer(response, encoding='gbk')
            writer.writerow(EN_CN_MAPPING.values())
            for data in plc_json:
                writing_res = list()
                for en_name in EN_CN_MAPPING.keys():
                    writing_res.append(data.get(en_name, '数据不存在'))
                writer.writerow(writing_res)

    print(response)
    return response
