from satellite.slack_utils import post_message_to_slack
from push_notifications.models import TickerMovementRule, NotificationSubscriber, RuleSubscription, TICKER_MOVEMENT_CONDITIONS
from satellite.models import Ticker


def reset_rules_status():
    for tmr in TickerMovementRule:
        tmr.is_satisfied_today = False
        tmr.message_today = None
        tmr.timestamp_satisfied = None
        tmr.save()


def process_rules():
    # find the rules that are satisfied
    # alert the subscribers. per user, compile one alert.

    # find the rules thare are satisfied
    newly_satisfied_rules = []
    for tmr in TickerMovementRule.objects.filter(is_satisfied_today=False).order_by('ticker_symbol'):

        is_satisfied = tmr.assess_is_satisfied()
        if is_satisfied:
            newly_satisfied_rules.append(tmr)

    print 'newly satisfied rules:', len(newly_satisfied_rules)
    print '\n'.join(['- %s' % nsr.message_today for nsr in newly_satisfied_rules])

    # group alerts by subscriber
    alert_messages_by_subscriber = {}
    rule_subscriptions = RuleSubscription.objects.filter(rule__in=newly_satisfied_rules)
    for rs in rule_subscriptions:
        if rs.subscriber not in alert_messages_by_subscriber:
            alert_messages_by_subscriber[rs.subscriber] = []
        alert_messages_by_subscriber[rs.subscriber].append(rs.rule.message_today)

    # alert the subscriber
    for subscriber in alert_messages_by_subscriber:
        message = '```' + '\n'.join(alert_messages_by_subscriber[subscriber]) + '```'
        post_message_to_slack(message_text=message, channel=subscriber.slack_handle, username='Ticker Alert', icon_emoji=':boom:')
        
    print 'users alerted:', len(alert_messages_by_subscriber)
    print ', '.join([s.name for s in alert_messages_by_subscriber])
