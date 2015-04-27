from django.conf.urls import patterns, url

from satellite import views, views_samples

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^movers/$', views.movers, name='movers'),
    url(r'^articles_by_service/$', views.articles_by_service, name='articles by service'),
    url(r'^info_by_scorecard/$', views.info_by_scorecard, name='info by scorecard'),
    url(r'^scorecard_index/$', views.scorecard_index, name="scorecard index"),
    url(r'^edit_notes/$', views.edit_notes, name="edit notes"),
    # url(r'^my_sample_view/$', views.my_sample_view, name="my sample view"),
    # some practice urls
    url(r'^all_the_bloody_services/$', views_samples.services_index, name='all_the_services'),
    url(r'^lola_rocks/$', views_samples.my_sample_view, name='lola_rocks'),
    url(r'^omg_articles/$', views_samples.articles_by_service, name='amazing_articles'),
    url(r'^articles_vomit/$', views_samples.grand_vision_articles, name='everything_about_articles'),
    url(r'^extras/$', views_samples.extra_views_homepage, name='extra_pages'),
    )
