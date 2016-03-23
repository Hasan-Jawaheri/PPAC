from django.conf.urls import patterns, include, url
from debug import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setinfo/', views.setinfo, name='setinfo'),
    url(r'^getinfo/', views.getinfo, name='getinfo'),
)
