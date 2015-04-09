from django.conf.urls import patterns, url

from satellite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^editors/$', views.editors, name='editors') 
)
