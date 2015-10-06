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

        for t in Ticker.objects.all():
            if t.tier == 1:
                print t.ticker_symbol, t.tier
                zero = 0
                t.tier = zero
                t.save()
                print t.ticker_symbol, t.tier
            else:
                continue
        t.tier == 0
        t.save()

    	print 'starting script'
        print 'pre-import: number of tickers in SOL with tier 1: %d' % get_count_of_tier_one_tickers()

        columns = defaultdict(list) # each value in each column is appended to a list

    	with open(TIERS_CSV, 'rU') as f:
    		reader = csv.DictReader(f) # read rows into a dictionary format
    		for row in reader: # read a row as {column1: value1, column2: value2,...}
    			for (k,v) in row.items(): # go over each column name and value
    				columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k

    	# get the tickers defined in the 'ticker' column.
    	# 	handle cases where a cell contains multiple tickers (separated by commas), eg "GOOGL, GOOG"
    	# 	remove duplicates (via set), and sort (via list)
    	tier_ones = set([t.strip().upper() for t in columns['ticker'] if t != ''])
    	elements_with_commas = set([t for t in tier_ones if ',' in t])
    	tier_ones = tier_ones - elements_with_commas
    	for e in elements_with_commas:
    		tokens = e.split(',')
    		for t in tokens:
    			tier_ones.add(t.strip())
    	tier_ones = list(tier_ones)
    	tier_ones.sort()

    	for ticker_symbol in tier_ones:
    		try:
    			ticker = Ticker.objects.get(ticker_symbol = ticker_symbol)
    			ticker.tier = 1
    			ticker.save()
    		except:
    			print '%s is not in SOL' % ticker_symbol

        print 'post-import: number of tickers in SOL with tier 1: %d' % get_count_of_tier_one_tickers()
    	print 'finished script'
