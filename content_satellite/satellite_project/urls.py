from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('satellite.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sol/', include('satellite.urls')),
    url(r'^alerts/', include('push_notifications.urls')),
    url(r'^apps/risk_ratings/', include('risk_ratings.urls', namespace='risk_ratings')),
)
