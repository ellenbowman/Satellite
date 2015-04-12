from django.contrib import admin

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard


class TickerAdmin(admin.ModelAdmin):
	list_display = ['ticker_symbol','daily_percent_change','company_name','exchange_symbol','services','scorecards','num_followers',
	'earnings_announcement','notes']
	#list_filter = ['num_services']
	search_fields = ['ticker_symbol', 'instrument_id','company_name']

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
	list_display = ['title', 'author', 'date_pub', 'service', 'ticker', 'url']
	list_filter = ['service', 'author',]
	search_fields = ['ticker__ticker_symbol', 'title',]

admin.site.register(Article, ArticleAdmin)
