from django.conf.urls import patterns, url

from satellite import views, views_samples

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^editors/$', views.editors, name='editors'),


    # some practice urls
    url(r'^all_the_bloody_services/$', views_samples.services_index, name='all_the_services'),
    url(r'^lola_rocks/$', views_samples.my_sample_view, name='lola_rocks'),
    url(r'^omg_articles/$', views_samples.articles_by_service, name='amazing_articles')

)