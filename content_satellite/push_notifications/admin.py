from django.contrib import admin
from models import NotificationSubscriber, IntradayBigMovementReceipt

class NotificationSubscriberAdmin(admin.ModelAdmin):
    model = NotificationSubscriber
    filter_horizontal = ['services',]
    list_display = ['name','slack_handle', 'tickers_csv']
    search_fields = ['name','slack_handle','email_address']

admin.site.register(NotificationSubscriber, NotificationSubscriberAdmin)

class IntradayBigMovementReceiptAdmin(admin.ModelAdmin):
    model = IntradayBigMovementReceipt
    list_display = ['ticker', 'percent_change', 'timestamp']
    search_fields = ['ticker',]

admin.site.register(IntradayBigMovementReceipt, IntradayBigMovementReceiptAdmin)
