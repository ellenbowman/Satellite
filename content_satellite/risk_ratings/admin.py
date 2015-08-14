from django.contrib import admin
from models import Ticker, TickerProfile, Questionnaire, Question, Hint, RiskRatingRecord, Feedback, RiskRatingDraft, DataImportLog


class TickerAdmin(admin.ModelAdmin):
    model = Ticker
    list_display = ['symbol','company_name', 'instrument_id']
    search_fields = ['symbol','company_name']

admin.site.register(Ticker, TickerAdmin)

class TickerProfileAdmin(admin.ModelAdmin):
    model = TickerProfile
    list_display = ['ticker', 'hq_country', 'net_income_ltm', 'free_cash_flow_ltm', 'market_cap', 'beta_ltm']
    search_fields = ['ticker__symbol',]

admin.site.register(TickerProfile,TickerProfileAdmin)

admin.site.register(Questionnaire)

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['questionnaire', 'list_order','label', 'text', 'hint']
    list_filter = ('questionnaire','hint')
    search_fields = ['label','text']

admin.site.register(Question, QuestionAdmin)

admin.site.register(Hint)

admin.site.register(RiskRatingRecord)

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ['name', 'email', 'timestamp']

admin.site.register(Feedback, FeedbackAdmin)

class RiskRatingDraftAdmin(admin.ModelAdmin):
    model = RiskRatingDraft
    list_display = ['timestamp', 'ticker_symbol', 'questionnaire_name', 'crushability_count']

admin.site.register(RiskRatingDraft, RiskRatingDraftAdmin)

class DataImportLogAdmin(admin.ModelAdmin):
    model = DataImportLog

admin.site.register(DataImportLog, DataImportLogAdmin)
