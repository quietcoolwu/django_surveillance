from django.http import HttpResponse
from django.shortcuts import render
from video.models import Article
from datetime import datetime
from django.http import Http404


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


def video3(request):
    return render(request, 'video3.html')


def env(request):
    return render(request, 'env.html')
