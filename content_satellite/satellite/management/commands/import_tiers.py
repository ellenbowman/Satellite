'''
Assigns tier status to Tickers, given a spreadsheet where the first column is named 'ticker' and contains Ticker symbols.
'''
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
import csv
from collections import defaultdict

TIERS_CSV = 'satellite/management/data/tiers.csv'

def get_count_of_tier_one_tickers():
    return len(Ticker.objects.filter(tier=1))

class Command(BaseCommand):

    def handle(self, *args, **options):
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

    	print 'starting script'
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
                        ticker.save()
                    except:
                        print '%s tier status cannot be updated' % ticker_symbol
         
        """
        EB work-in-progress note: the above solution does not convert tickers to U/C and remove commas like the old code did.
        However, I plan to maintain the tiers spreadsheet so that there will only ever be one U/C ticker per field.
        So I will leave that problem for now.
        Also I need to find out how to make it so I can concat service names into tier_status with commas between names
        but no comma on the end.
        Two tickers are erroring: ZG and PYPL. 
        """

        print 'post-import: number of tickers in SOL with tier 1: %d' % get_count_of_tier_one_tickers()
    	print 'finished script'
