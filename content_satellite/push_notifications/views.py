from django.shortcuts import render
from django.utils import timezone
from push_notifications.models import IntradayBigMovementReceipt, NotificationSubscriber, INTRADAY_THRESHOLD
from push_notifications.forms import SubscriberForm


def index(request):

    if request.POST:
        form = SubscriberForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            print data

            subscriber = NotificationSubscriber(slack_handle = data['slack_handle'])
            if 'tickers_csv' in data:
                subscriber.tickers_csv = data['tickers_csv']
            subscriber.save()
            if 'services' in data:
                for s in data['services']:
                    subscriber.services.add(s)
                subscriber.save()
            # reset the form
            form = SubscriberForm()

    else:
        form = SubscriberForm()

    context = {
        'page_title': 'Intraday Movement Notifications',
        'receipts': IntradayBigMovementReceipt.objects.filter(timestamp__gt=timezone.now().date()).order_by('-timestamp'),
        'subscribers': NotificationSubscriber.objects.all().order_by('slack_handle'),
        'threshold':INTRADAY_THRESHOLD,
        'form': form
    }

    return render(request, 'push_notifications/index.html', context)
