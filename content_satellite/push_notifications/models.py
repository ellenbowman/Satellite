from django.utils import timezone
from django.db import models
from satellite.models import Ticker

TICKER_INTRADAY_MOVEMENT_GREATER_THAN = 'gt'
TICKER_INTRADAY_MOVEMENT_LESS_THAN = 'lt'

TICKER_MOVEMENT_CONDITIONS = (
    (TICKER_INTRADAY_MOVEMENT_GREATER_THAN, 'better than'),
    (TICKER_INTRADAY_MOVEMENT_LESS_THAN, 'worse than')
)

# what are the alert-worthy conditions?
class TickerMovementRule(models.Model):

    ticker_symbol = models.CharField(max_length=10)
    threshold = models.IntegerField(default=7, verbose_name="percent change")
    condition = models.CharField(choices=TICKER_MOVEMENT_CONDITIONS, max_length=5)
    is_satisfied_today = models.BooleanField(default=False, verbose_name='has the condition been satisfied today?')
    message_today = models.CharField(max_length=200, blank=True, null=True)
    timestamp_satisfied = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        # eg: 'AAPL: greater than 14%'  /  'COH: less than 4%'
        return "%s: %s %d%%" %  (self.ticker_symbol, self.get_condition_display(), self.threshold)


    def assess_is_satisfied(self):
        try:
            ticker = Ticker.objects.get(ticker_symbol=self.ticker_symbol)
        except Exception as e:
            print e
            # the rule doesn't correspond to a ticker in our system
            return False

        is_satisfied_today = False

        if self.condition == TICKER_INTRADAY_MOVEMENT_GREATER_THAN:
            is_satisfied_today = ticker.daily_percent_change > self.threshold
        elif self.condition == TICKER_INTRADAY_MOVEMENT_LESS_THAN:
            is_satisfied_today = ticker.daily_percent_change < self.threshold

        if is_satisfied_today:
            self.is_satisfied_today = True
            if ticker.daily_percent_change > 0:
                self.message_today = "%s is up %d%%" % (ticker.ticker_symbol, ticker.daily_percent_change)
            else:
                self.message_today = "%s is down %d%%" % (ticker.ticker_symbol, ticker.daily_percent_change)
            if ticker.services_for_ticker:
                self.message_today += " _(%s)_" % ticker.services_for_ticker

            self.timestamp_satisfied = timezone.now()
            self.save()

        return is_satisfied_today


# contact info - how a user wants to be alerted
class NotificationSubscriber(models.Model):
    name = models.CharField(max_length=100, verbose_name='Contact Name')
    slack_handle = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.slack_handle

# pair a user and a condition; a user may sign up to be alerted for many conditions,
# and a condition may alert many users
class RuleSubscription(models.Model):
    rule = models.ForeignKey(TickerMovementRule)
    subscriber = models.ForeignKey(NotificationSubscriber)
    is_preference_asap = models.BooleanField(default=True, verbose_name='push an alert as soon as the condition is satisfied (vs end of day)')

    def __unicode__(self):
        return "%s: %s" % (self.subscriber, self.rule)
