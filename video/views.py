#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
from datetime import datetime

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from video.models import Article


# Create your views here.
def home(request):
    post_list = Article.objects.all()
    return render(request, 'home.html', {'post_list': post_list})


def test(request):
    return render(request, 'test.html', {'current_time': datetime.now()})


def detail(request, _id):
    try:
        post = Article.objects.get(id=str(_id))

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
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="today.csv"'
    print(response, type(response))

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
