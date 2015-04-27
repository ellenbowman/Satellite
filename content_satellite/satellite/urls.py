from django.conf.urls import patterns, url

from satellite import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^movers/$', views.movers, name='movers'),
    url(r'^articles_by_service/$', views.articles_by_service, name='articles by service'),
    url(r'^info_by_scorecard/$', views.info_by_scorecard, name='info by scorecard'),
    url(r'^scorecard_index/$', views.scorecard_index, name="scorecard index"),
    url(r'^edit_notes/$', views.edit_notes, name="edit notes"),
#    url(r'^my_sample_view/$', views.my_sample_view, name="my sample view"),
    )
