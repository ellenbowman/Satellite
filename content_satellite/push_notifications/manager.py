from django.db.models import Q
from django.utils import timezone
from satellite.slack_utils import post_message_to_slack
from push_notifications.models import INTRADAY_THRESHOLD, IntradayBigMovementReceipt, NotificationSubscriber
from satellite.models import Ticker, Service


def process_rules():
    # find tickers that newly satisfy the threshold value
    # alert subscribers that follow any of those tickers

    # find tickers that satisfy the threshold value
    tickers_with_big_movement = Ticker.objects.filter( Q(daily_percent_change__gt=INTRADAY_THRESHOLD) | Q(daily_percent_change__lt=-1*INTRADAY_THRESHOLD)).order_by('ticker_symbol')

    # filter down to the ones that have hit the threshold for the first time today
    # create a receipt for each of these newly-detected big movers
    new_movers_receipts = []
    for t in tickers_with_big_movement:
        matches_for_today = IntradayBigMovementReceipt.objects.filter(ticker=t, timestamp__gt=timezone.now().date())
        if not matches_for_today:
            new_movers_receipts.append(IntradayBigMovementReceipt.create(t, t.daily_percent_change))

    print 'newly-detected big movers: %d (%s)' % (len(new_movers_receipts), ', '.join([nmr.ticker.ticker_symbol for nmr in new_movers_receipts]))

    if len(new_movers_receipts) == 0:
        return

    # for each active subscriber, figure out which of the newly-detected big movers match his interests
    for subscriber in NotificationSubscriber.objects.filter(is_active=True):
        tickers_for_subscriber = [t.strip() for t in subscriber.tickers_csv.upper().split(',')]
        subscriber_services = [s.pretty_name.strip() for s in subscriber.services.all()]

        messages_for_subscriber = []
        for r in new_movers_receipts:
            if r.ticker.ticker_symbol in tickers_for_subscriber:
                messages_for_subscriber.append(r.message)
            elif r.ticker.services_for_ticker:
                ticker_services = [s.strip() for s in r.ticker.services_for_ticker.split(',')]
                if set(subscriber_services) & set(ticker_services):
                    messages_for_subscriber.append(r.message)

        if messages_for_subscriber:
            message_text = '```' + '\n'.join(messages_for_subscriber) + '```'
            post_message_to_slack(message_text=message_text, channel=subscriber.slack_handle, username='Ticker Alert', icon_emoji=':boom:')

            print 'alerted %s: %s' % (subscriber.slack_handle, message_text)
