from django.core.management.base import BaseCommand, CommandError
from satellite.models import Service
from push_notifications.models import NotificationSubscriber

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        try:
            satellite_admin_user = NotificationSubscriber.objects.get(slack_handle='@lchung')
        except:
            satellite_admin_user = NotificationSubscriber.objects.create(slack_handle='@lchung', name='Satellite Admin', email_address='lchung@fool.com', tickers_csv='')
            for s in Service.objects.all():
                satellite_admin_user.services.add(s)
            satellite_admin_user.save()

        print 'finished script'
