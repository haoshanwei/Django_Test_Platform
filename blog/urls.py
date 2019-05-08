# coding:utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.blog_title ,{"template_name":"blog/titles.html"},name='blog_title'),
    url(r'(?P<article_id>\d)/$',views.blog_article,name = "blog_article"),
]