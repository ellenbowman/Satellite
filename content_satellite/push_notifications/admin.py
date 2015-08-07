from django.contrib import admin
from models import TickerMovementRule, NotificationSubscriber, RuleSubscription

class TickerMovementRuleAdmin(admin.ModelAdmin):
    model = TickerMovementRule
    list_display = ['ticker_symbol', 'threshold', 'is_satisfied_today']
    search_fields = ['ticker_symbol',]
    list_filter = ['is_satisfied_today',]

admin.site.register(TickerMovementRule, TickerMovementRuleAdmin)

admin.site.register(NotificationSubscriber)

class RuleSubscriptionAdmin(admin.ModelAdmin):
    model = RuleSubscription
    list_display = ['subscriber','rule', 'is_preference_asap',]

admin.site.register(RuleSubscription, RuleSubscriptionAdmin)
