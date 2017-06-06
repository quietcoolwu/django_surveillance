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

from __future__ import absolute_import

from dashing.utils import router
from django.conf.urls import include, url
from django.contrib import admin

from video import views as video_views

from .widgets import NewClientsWidget, PLCDataWidget

# from django.views.generic.base import RedirectView


router.register(NewClientsWidget, 'new_users_widget')
router.register(PLCDataWidget, 'plc_data_widget')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^video/', video_views.video),
    url(r'^p2p_video/', video_views.p2p_video),
    url(r'^home/', video_views.home, name='home'),
    url(r'^$', video_views.prod_index, name='prod_index'),
    url(r'^(?P<id>\d+)/$', video_views.detail, name='detail'),
    url(r'^env/', video_views.env),
    url(r'^download_csv/$', video_views.download_csv),
    url(r'^dashboard/', include(router.urls), name='dashboard'),
    # url(r'^$', RedirectView.as_view(url='dashboard/'), name='index')
]
