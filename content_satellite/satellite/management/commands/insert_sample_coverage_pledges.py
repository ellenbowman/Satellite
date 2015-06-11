'''
insert fake CoverageType records
'''
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker, COVERAGE_CHOICES, CoverageType, Service
import random

class Command(BaseCommand):
    help = 'inserts fake CoverageType records. for every ticker, for each service that cares about the ticker, ' \
           'randomly pick one of the coverage types (Earnings Preview, 5 and 3, etc) and create a CoverageType record' \
           'for that trio of ticker, service, and coverage type.'

    def handle(self, *args, **options):
        print 'starting script'

        num_inserts = 0

        for t in Ticker.objects.all():
            for s in Service.objects.all():
                if t.services_for_ticker is not None and s.pretty_name in t.services_for_ticker:
                    randomly_selected_coverage_type = random.randint(0, len(COVERAGE_CHOICES)-1)   # https://docs.python.org/2/library/random.html

                    coverage_type = CoverageType(ticker=t, service=s, coverage_type=randomly_selected_coverage_type)
                    coverage_type.save()
                    print 'inserted coverage type %s %s %s' % (t.ticker_symbol, s.pretty_name, randomly_selected_coverage_type)
                    num_inserts += 1

        print 'finished script. num inserts: %d' % num_inserts
