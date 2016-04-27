'''
Imports data from a spreadsheet that has Conviction Cloud data.
'''

import datetime
import csv
from django.core.management.base import BaseCommand, CommandError


from satellite.models import Ticker, Scorecard, ServiceTake, DataHarvestEventLog
from django.conf import settings
from satellite.models import Article, Service, Ticker, DATA_HARVEST_TYPE_IMPORT_CLOUD_DATA
from collections import defaultdict

CLOUD_CSV = 'satellite/management/data/cloud.csv'

#def get_count_of_tier_one_tickers():
#    return len(Ticker.objects.filter(tier=1))

class Command(BaseCommand):
    help = "Imports cloud captain, points, sector, instrument ID from cloud spreadsheet"

    def handle(self, *args, **options):
        print "Let's do this"

        event_log = DataHarvestEventLog()
        event_log.data_type = DATA_HARVEST_TYPE_IMPORT_CLOUD_DATA
        event_log.notes = 'running'
        event_log.save()

        script_start_time = datetime.datetime.now()
        notes = ''

    	print 'starting cloud import'

        #columns = defaultdict(list) # each value in each column is appended to a list

    	with open(CLOUD_CSV, 'rU') as f:
    		reader = csv.DictReader(f) # read rows into a dictionary format
    		for row in reader: # read a row as {column1: value1, column2: value2,...}
                    ticker_symbol = str(row['ticker']).upper()
                    cloud_captain = str(row['captain'])
                    print cloud_captain
                    points = int(row['points'])
                    print points
                    sector = str(row['sector'])
                    print sector
                    instrument_id = int(row['instrument_id'])
                    print instrument_id

                    try:
                        ticker = Ticker.objects.get(ticker_symbol = ticker_symbol)
                        ticker.cloud_captain = cloud_captain
                        ticker.points = points
                        ticker.sector = sector
                        ticker.instrument_id = instrument_id
                        print ticker_symbol, ticker.cloud_captain, ticker.points, ticker.sector, ticker.instrument_id
                        ticker.save()
                    except:
                        print '%s cloud status cannot be updated' % ticker_symbol
         
        script_end_time = datetime.datetime.now()
        total_seconds = (script_end_time - script_start_time).total_seconds()

        print 'time elapsed: %d seconds' %  total_seconds
        event_log.notes = notes         
        event_log.save()

        print 'finished script'