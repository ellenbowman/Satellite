'''
clear all notes fields for a new earnings season
'''
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker


class Command(BaseCommand):
    help = 'Clears all notes fields for tickers'

    def handle(self, *args, **options):
    	print 'starting script'

        print 'how many tickers?', len(Ticker.objects.all())
    	all_tickers = Ticker.objects.all()


    	for t in all_tickers:
            t.notes = ""
            t.save()

    	print 'finished script'
