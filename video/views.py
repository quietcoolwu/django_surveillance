from django.http import HttpResponse
from django.shortcuts import render
from video.models import Article
from datetime import datetime


# Create your views here.
def home(request):
    post_list = Article.objects.all()
    return render(request, 'home.html', {'post_list': post_list})


def test(request):
    return render(request, 'test.html', {'current_time': datetime.now()})


def video1(request):
    return render(request, 'video1.html')


def video2(request):
    return render(request, 'video2.html')

# def detail(request, my_args):
#     post = Article.objects.all()[int(my_args)]
#     str1 = ("title = %s, category = %s, date_time = %s, content = %s"
#             % (post.title, post.category, post.date_time, post.content))
#     return HttpResponse(str1)
