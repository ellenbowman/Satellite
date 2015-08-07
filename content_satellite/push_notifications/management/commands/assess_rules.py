from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from push_notifications.manager import process_rules

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        process_rules()

        print 'finished script'
