"""d10server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from dashing.utils import router
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from .widgets import NewClientsWidget

router.register(NewClientsWidget, 'new_users_widget')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^video/', 'video.views.video'),
    url(r'^$', 'video.views.home', name='home'),
    url(r'^(?P<id>\d+)/$', 'video.views.detail', name='detail'),
    url(r'^env/$', 'video.views.env'),
    url(r'^dashboard/', include(router.urls), name='dashboard'),
    url(r'^$', RedirectView.as_view(url='dashboard/'), name='index')
]
