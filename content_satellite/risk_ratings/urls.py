from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create', views.create_risk_rating, name='create_risk_rating'),
    url(r'^log', views.activity_log_index, name='view_log'),
    url(r'^generate_markup', views.generate_markup, name='generate_markup'),
    url(r'^feedback/', views.contact, name='contact'),
]
