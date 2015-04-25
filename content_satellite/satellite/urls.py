from django.conf.urls import patterns, url

from satellite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^movers/$', views.movers, name='movers'),
    url(r'^articles_by_service/$', views.articles_by_service, name='articles by service'),
    url(r'^service_index/$', views.service_index, name="service index"),
    )
