from django.contrib import admin

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard

class TickerAdmin(admin.ModelAdmin):
	list_display = ['ticker_symbol', 'exchange_symbol','num_followers','num_scorecards','num_services','earnings_announcement','percent_change_historical','company_name',]
	search_fields = ['ticker_symbol', 'instrument_id',]

admin.site.register(Ticker, TickerAdmin)

admin.site.register(Service)

class ScorecardAdmin(admin.ModelAdmin):
	list_display = ['name', 'service', 'pretty_name']

admin.site.register(Scorecard, ScorecardAdmin)

class ServiceTakeAdmin(admin.ModelAdmin):
	list_display = ['ticker', 'open_date', 'scorecard', 'action', 'is_core', 'is_newest', 'is_first']
	list_filter = ['scorecard', 'scorecard__service','is_core', 'is_first', 'is_newest']
	search_fields = ['ticker__ticker_symbol',]

admin.site.register(ServiceTake, ServiceTakeAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'date_pub', 'url', 'service', 'ticker']
	list_filter = ['service', 'author',]
	search_fields = ['ticker__ticker_symbol', 'title',]

admin.site.register(Article, ArticleAdmin)
