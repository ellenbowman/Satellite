from django.conf.urls import patterns, url

from satellite import views, views_2

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^tickers/$', views.ticker_overview, name='ticker_overview'),
    url(r'^tickers/(?P<ticker_symbol>\S+)/$', views.ticker_detail, name='ticker_detail'),
    url(r'^upcoming_earnings/$', views_2.upcoming_earnings, name='upcoming_earnings'),
    #url(r'^ticker_world/next_week/$', views.next_week, name='next_week'),
    url(r'^tiered_stocks/$', views.tiered_stocks, name='tiered_stocks'),
    url(r'^coverage_overview/$', views.coverage_overview, name='coverage_overview'),
    url(r'^service_overview/$', views.service_overview, name="service_overview"),
    url(r'^data_freshness/$', views_2.data_freshness_index, name="data_freshness"),
    url(r'^author_bylines/$', views_2.get_author_bylines_index, name='author_bylines'),
    url(r'^flagged_recs/$', views_2.get_flagged_recs_index, name='flagged_recs'),    
    url(r'^flagged_recs_csv/$', views_2.get_flagged_recs_as_csv, name='flagged_recs_as_csv'),
    url(r'^articles_index/$', views_2.articles_index, name='articles_index'),
    url(r'^json_blob_for_ticker/$', views_2.ticker_lookup, name='json_blob'),
    )
