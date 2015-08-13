from django.contrib import admin
from models import NotificationSubscriber, IntradayBigMovementReceipt

class NotificationSubscriberAdmin(admin.ModelAdmin):
    model = NotificationSubscriber
    filter_horizontal = ['services',]
    list_filter = ['is_active']
    list_display = ['slack_handle', 'tickers_csv', 'is_active']
    search_fields = ['slack_handle',]

admin.site.register(NotificationSubscriber, NotificationSubscriberAdmin)

class IntradayBigMovementReceiptAdmin(admin.ModelAdmin):
    model = IntradayBigMovementReceipt
    list_display = ['ticker', 'percent_change', 'timestamp']
    search_fields = ['ticker',]

admin.site.register(IntradayBigMovementReceipt, IntradayBigMovementReceiptAdmin)
