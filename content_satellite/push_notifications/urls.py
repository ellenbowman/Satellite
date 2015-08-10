from django.conf.urls import patterns, url

from push_notifications import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='alerts_index'),
    )
