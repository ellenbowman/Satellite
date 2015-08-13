from django.conf.urls import patterns, url

from push_notifications import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='alerts_index'),
    url(r'^suspend/(?P<subscriber_id>\S+)/(?P<slack_handle>\S+)$', views.suspend_subscription, name='suspend_subscription'),
    url(r'^resume/(?P<subscriber_id>\S+)/(?P<slack_handle>\S+)$', views.resume_subscription, name='resume_subscription'),
    )
