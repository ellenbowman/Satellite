from django.contrib import admin
from django.db import models

from satellite.models import Ticker, Service, ServiceTake, Article, Scorecard, DataHarvestEventLog, BylineMetaData, CoverageType


class TickerAdmin(admin.ModelAdmin):
	list_display = ['ticker_symbol','company_name','daily_percent_change','exchange_symbol','services','scorecards','tier', 'tier_status',
	'earnings_announcement','notes', 'cloud_captain', 'points', 'sector', 'instrument_id']
	search_fields = ['ticker_symbol', 'instrument_id','company_name']

admin.site.register(Ticker, TickerAdmin)

admin.site.register(Service)

class CoverageTypeAdmin(admin.ModelAdmin):
	list_display = ['coverage_type','service','ticker']
	list_filter = ['service','coverage_type']
	search_fields = ['ticker__ticker_symbol',]

admin.site.register(CoverageType, CoverageTypeAdmin)

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
	list_filter = ['service']
	search_fields = ['ticker__ticker_symbol', 'title',]

admin.site.register(Article, ArticleAdmin)

class DataHarvestEventLogAdmin(admin.ModelAdmin):
	list_display = ['date_type_pretty_name', 'date_started', 'date_finished', 'notes']

admin.site.register(DataHarvestEventLog, DataHarvestEventLogAdmin)	

class BylineMetaDataAdmin(admin.ModelAdmin):
	list_display = ['byline', 'services', 'tickers']

admin.site.register(BylineMetaData, BylineMetaDataAdmin)