from django.conf.urls import patterns, url

from satellite import views, views_samples, views_data_freshness

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^movers/$', views.movers, name='movers'),
    url(r'^articles_by_service/$', views.articles_by_service, name='articles by service'),
    url(r'^ticker_world/$', views.ticker_world, name='ticker_world'),
    url(r'^scorecard_index/$', views.scorecard_index, name="scorecard index"),
    # url(r'^my_sample_view/$', views.my_sample_view, name="my sample view"),
    url(r'^data_freshness/$', views_data_freshness.data_freshness_index, name="data_freshness"),
    url(r'^author_bylines/$', views_samples.get_author_bylines_index, name='author_bylines'),
    # some practice urls
    url(r'^all_the_bloody_services/$', views_samples.services_index, name='all_the_services'),
    url(r'^lola_rocks/$', views_samples.my_sample_view, name='lola_rocks'),
    url(r'^omg_articles/$', views_samples.articles_by_service, name='amazing_articles'),
    url(r'^articles_index/$', views_samples.grand_vision_articles, name='everything_about_articles'),
    url(r'^extras/$', views_samples.extra_views_homepage, name='extra_pages'),
    )
