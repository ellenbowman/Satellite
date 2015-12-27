import json
from pytz import timezone
from django.db import models
from datetime import datetime

EASTERN_TZ = timezone('US/Eastern')

class Ticker(models.Model):
    
    ticker_symbol = models.CharField(max_length=5, verbose_name='symbol')
    exchange_symbol = models.CharField(max_length=10, verbose_name='exchange')
    instrument_id = models.IntegerField(default=0)
    num_followers = models.IntegerField(default=0, verbose_name='One followers')
    earnings_announcement = models.DateField(null=True, blank=True, verbose_name='next earnings date')
    daily_percent_change = models.DecimalField(max_digits=11, default=0, decimal_places=2, verbose_name='Daily % change')
    percent_change_historical = models.DecimalField(max_digits=11, decimal_places=3, verbose_name='50D%Change')
    company_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='name')
    notes = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Notes')
    scorecards_for_ticker = models.CharField(max_length=200, null=True, blank=True, verbose_name='scorecards for ticker')
    services_for_ticker = models.CharField(max_length=200, null=True, blank=True, verbose_name='services for ticker')   
    tier = models.IntegerField(default=0)
    tier_status = models.CharField(max_length=50, null=True, blank=True, verbose_name='tier status')
    analysts_for_ticker = models.CharField(max_length=500, null=True, blank=True, verbose_name='analysts for ticker')
    promised_coverage = models.TextField(max_length=500, null=True, blank=True, verbose_name='promised coverage')

    def __unicode__(self):
        return self.ticker_symbol


    class Meta:
        ordering = ['ticker_symbol']


    def scorecards(self):
        """ which scorecards have this ticker? """

        service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

        scorecards_represented = set()
        for service_take in service_takes_on_this_ticker:
            scorecards_represented.add(service_take.scorecard.pretty_name)
        return ", ".join(scorecards_represented)

    def services(self):
        """how many services have this ticker?"""

        service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

        services_represented = set()
        for service_take in service_takes_on_this_ticker:
            services_represented.add(service_take.scorecard.service.name)

        num_services = len(services_represented)
        return num_services


class DataImportLog(models.Model):
    ticker_count = models.IntegerField()
    timestamp = models.DateTimeField()

    @staticmethod
    def get_last_timestamp():
        if DataImportLog.objects.count():
            return DataImportLog.objects.all().order_by('-timestamp')[0].timestamp

        return None

    def save(self, *args, **kwargs):
        # update timestamps
        self.timestamp = datetime.now(EASTERN_TZ)
        return super(DataImportLog, self).save(*args, **kwargs)
