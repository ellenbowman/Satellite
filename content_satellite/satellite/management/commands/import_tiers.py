'''
Assigns tier status to Tickers, given a spreadsheet where the first column is named 'ticker' and contains Ticker symbols.
'''

import datetime
import csv
from django.core.management.base import BaseCommand, CommandError


from satellite.models import Ticker, Scorecard, ServiceTake
from django.conf import settings
from satellite.models import Article, Service, Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_IMPORT_TIERS
from collections import defaultdict

TIERS_CSV = 'satellite/management/data/tiers.csv'

def get_count_of_tier_one_tickers():
    return len(Ticker.objects.filter(tier=1))

class Command(BaseCommand):
    help = "Imports core, first, BBN, new rec information for tickers."

    def handle(self, *args, **options):
        print "Getting tier status"

        event_log = DataHarvestEventLog()
        event_log.data_type = DATA_HARVEST_TYPE_IMPORT_TIERS
        event_log.notes = 'importing tier information'
        event_log.save()

        script_start_time = datetime.datetime.now()
        notes = ''

        print 'start delete'
        for t in Ticker.objects.all():
            if t.tier_status != None:
                t.tier_status = ''
                t.save()
            if t.tier == 1:
                t.tier_status = ''
                t.tier = 0
                t.save()
                print t.ticker_symbol, t.tier, t.tier_status
            else:
                continue
        t.tier == 0
        t.save()

        print 'end delete'

    	print 'starting tier import'
        print 'pre-import: number of tickers in SOL with tier 1: %d' % get_count_of_tier_one_tickers()

        columns = defaultdict(list) # each value in each column is appended to a list

    	with open(TIERS_CSV, 'rU') as f:
    		reader = csv.DictReader(f) # read rows into a dictionary format
    		for row in reader: # read a row as {column1: value1, column2: value2,...}
                    ticker_symbol = str(row['ticker'])
                    service = str(row['service'])
                    try:
                        ticker = Ticker.objects.get(ticker_symbol = ticker_symbol)
                        ticker.tier = 1
                        ticker.tier_status += ' %s,' % service
                        print ticker.tier_status
                        ticker.save()
                    except:
                        print '%s tier status cannot be updated' % ticker_symbol
         
        """
        EB work-in-progress note: the above solution does not convert tickers to U/C and remove commas like the old code did.
        However, I plan to maintain the tiers spreadsheet so that there will only ever be one U/C ticker per field.
        So I will leave that problem for now.
        Also I need to find out how to make it so I can concat service names into tier_status with commas between names
        but no comma on the end.
        """

        notes = 'updated tier status'

        script_end_time = datetime.datetime.now()
        total_seconds = (script_end_time - script_start_time).total_seconds()

        print 'time elapsed: %d seconds' %  total_seconds
        event_log.notes = notes         
        event_log.save()

        print 'finished script'