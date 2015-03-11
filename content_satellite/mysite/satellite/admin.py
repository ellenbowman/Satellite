from django.contrib import admin

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard

admin.site.register(Ticker)

admin.site.register(Service)

admin.site.register(Article)

class ScorecardAdmin(admin.ModelAdmin):
	list_display = ['name', 'service', 'pretty_name']

admin.site.register(Scorecard, ScorecardAdmin)

class ServiceTakeAdmin(admin.ModelAdmin):
	list_display = ['ticker', 'open_date', 'scorecard', 'action', 'is_core', 'is_newest', 'is_first']
	list_filter = ['scorecard','is_core', 'is_first', 'is_newest']
	search_fields = ['ticker__ticker_symbol',]

admin.site.register(ServiceTake, ServiceTakeAdmin)