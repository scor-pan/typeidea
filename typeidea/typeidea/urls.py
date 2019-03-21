"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings 

from blog.views import (
        IndexView, CategoryView, TagView,
        PostDetailView, SearchView, AuthorView,
)
from comment.views import CommentView
from config.views import LinkListView
from typeidea.custom_site import custom_site
from typeidea.settings.base import DEBUG as settings_DEBUG

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'), 
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^search/$', SearchView.as_view(),name='search'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^super-admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

   # r'^category/(?P<category_id>\d+)/$': 带group的正则表达式，把URL这个位置的字符作为名为category_id的参数传递给post_list函数。  第二个参数定义用来处理请求的函数。  第三个参数定义默认传递过去的函数，也就是无论什么请求，都会传递{'example': 'nop'}到post_list中。第四个参数是这个URL的名称
    
