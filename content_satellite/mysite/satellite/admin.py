from django.contrib import admin

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard

admin.site.register(Ticker)

admin.site.register(Service)

admin.site.register(ServiceTake)

admin.site.register(Article)

admin.site.register(Scorecard)
