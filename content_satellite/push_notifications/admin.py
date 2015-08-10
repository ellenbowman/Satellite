from django.contrib import admin
from models import NotificationSubscriber, IntradayBigMovementReceipt

class NotificationSubscriberAdmin(admin.ModelAdmin):
    model = NotificationSubscriber
    filter_horizontal = ['services',]
    list_display = ['slack_handle', 'tickers_csv']
    search_fields = ['slack_handle',]

admin.site.register(NotificationSubscriber, NotificationSubscriberAdmin)

class IntradayBigMovementReceiptAdmin(admin.ModelAdmin):
    model = IntradayBigMovementReceipt
    list_display = ['ticker', 'percent_change', 'timestamp']
    search_fields = ['ticker',]

admin.site.register(IntradayBigMovementReceipt, IntradayBigMovementReceiptAdmin)
