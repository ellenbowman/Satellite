from django.utils import timezone
from django.db import models
from satellite.models import Ticker, Service

INTRADAY_THRESHOLD = 7.5

class IntradayBigMovementReceipt(models.Model):
    '''
    generated the first time in a day that a ticker moves beyond the INTRADAY_THRESHOLD
    '''
    ticker = models.ForeignKey(Ticker)
    percent_change = models.DecimalField(max_digits=7, default=0, decimal_places=2, verbose_name='% change at time of alert')
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, ticker, percent_change):
        receipt = cls(ticker=ticker, percent_change=ticker.daily_percent_change, timestamp=timezone.now())
        receipt.save()
        return receipt

    @property
    def message(self):
        message_text = '%s (%s): %.2f%%' % (self.ticker.company_name[:35], self.ticker.ticker_symbol, self.percent_change)
        if self.ticker.services_for_ticker:
            message_text += ' (%s)' % self.ticker.services_for_ticker
        return message_text


class NotificationSubscriber(models.Model):
    '''
    who wants to be alerted, and the services and extra tickers they wish to follow
    '''
    slack_handle = models.CharField(max_length=30)
    tickers_csv = models.CharField(max_length=400, blank=True, null=True)
    services = models.ManyToManyField(Service, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.slack_handle

    @property
    def services_display_string(self):
        return ', '.join([s.pretty_name for s in self.services.all().order_by('pretty_name')])
