from django.conf.urls import patterns, url

from satellite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^movers/$', views.movers, name='movers') 
)
