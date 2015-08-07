from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from push_notifications.manager import reset_rules_status

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        reset_rules_status()

        print 'finished script'
