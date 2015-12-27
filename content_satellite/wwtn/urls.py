from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create', views.wwtn, name='wwtn'),
    url(r'^log', views.activity_log_index, name='view_log'),
    url(r'^generate_markup', views.generate_markup, name='generate_markup'),
]
