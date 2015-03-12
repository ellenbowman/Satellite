from django.contrib import admin

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard

admin.site.register(Ticker)

admin.site.register(Service)

class ScorecardAdmin(admin.ModelAdmin):
	list_display = ['name', 'service', 'pretty_name']

admin.site.register(Scorecard, ScorecardAdmin)

class ServiceTakeAdmin(admin.ModelAdmin):
	list_display = ['ticker', 'open_date', 'scorecard', 'action', 'is_core', 'is_newest', 'is_first']
	list_filter = ['scorecard', 'scorecard__service','is_core', 'is_first', 'is_newest']
	search_fields = ['ticker__ticker_symbol',]

admin.site.register(ServiceTake, ServiceTakeAdmin)

#what else.... it'd be cool if in the satellite's admin.py,
#we had custom admins for the Article and Ticker,

class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'date_pub', 'url', 'service', 'ticker']
	list_filter = ['service', 'author',]
	search_fields = ['ticker__ticker_symbol',]

admin.site.register(Article, ArticleAdmin)

#like how you already set up ScorecardAdmin so that additional columns
#are displayed, and ServiceTakeAdmin, so that additional columns are
#displayed AND you can filter AND you can search by ticker symbol