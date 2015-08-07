from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from push_notifications.models import TickerMovementRule, NotificationSubscriber, RuleSubscription, TICKER_INTRADAY_MOVEMENT_GREATER_THAN, TICKER_INTRADAY_MOVEMENT_LESS_THAN

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        # for each ticker in our system, add rules for whether it's gone up over 7%, and whether it's gone down more than 7%
        for t in Ticker.objects.all():
            if not TickerMovementRule.objects.filter(ticker_symbol=t.ticker_symbol):
                TickerMovementRule.objects.create(ticker_symbol=t.ticker_symbol, threshold=-7, condition=TICKER_INTRADAY_MOVEMENT_LESS_THAN)
                TickerMovementRule.objects.create(ticker_symbol=t.ticker_symbol, threshold=7, condition=TICKER_INTRADAY_MOVEMENT_GREATER_THAN)

        try:
            satellite_admin_user = NotificationSubscriber.objects.get(slack_handle='@lchung')
        except:
            satellite_admin_user = NotificationSubscriber.objects.create(slack_handle='@lchung', name='Satellite Admin')

        subscriptions_for_satellite_admin = RuleSubscription.objects.filter(subscriber=satellite_admin_user)
        subscribed_rules = [rs.rule for rs in subscriptions_for_satellite_admin]
        for tmr in TickerMovementRule.objects.all():
            if tmr not in subscribed_rules:
                RuleSubscription.objects.create(rule=tmr, subscriber=satellite_admin_user)

        print 'finished script'

        print 'how many ticker movement rules?', TickerMovementRule.objects.count()
        print 'how many subscribers?', NotificationSubscriber.objects.count()
        print 'how many ticker movement rule subscriptions?', RuleSubscription.objects.count()
