from django.contrib import admin
from models import Ticker

class TickerAdmin(admin.ModelAdmin):
    model = Ticker
    list_display = ['symbol','company_name', 'instrument_id']
    search_fields = ['symbol','company_name']

admin.site.register(Ticker, TickerAdmin)

class DataImportLogAdmin(admin.ModelAdmin):
    model = DataImportLog

admin.site.register(DataImportLog, DataImportLogAdmin)
