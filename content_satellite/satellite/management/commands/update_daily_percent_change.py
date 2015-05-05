'''
update the 'daily_percent_change' field on all Ticker objects
'''
import urllib
import json
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_MARKET_DATA


def get_daily_percent_change(ticker_symbols_as_list):
	""" get the daily percent change, as reported by Yahoo Finance
	"""
	yahoo_finance_url = 'http://query.yahooapis.com/v1/public/yql'

	# when we make the request, pass along additional preferences, eg the SQL query
	ticker_symbols_as_string = ','.join(ticker_symbols_as_list)
	data = {'q': "select Symbol, PercentChange from yahoo.finance.quotes where symbol in (%s)" % ticker_symbols_as_string, 
	'format': 'json',
	'diagnostics':'false',
	'env': 'http://datatables.org/alltables.env',}

	encoded_data = urllib.urlencode(data)
	url = "%s?%s" % (yahoo_finance_url, encoded_data)

	yahoo_response = urllib.urlopen(url, timeout=5).read()
	yahoo_json = json.loads(yahoo_response)

	daily_percent_change_keyed_by_ticker_symbol = {}

	for quote_result in yahoo_json['query']['results']['quote']:

		symbol = quote_result['Symbol']  
		daily_percent_change = quote_result['PercentChange']  

		if daily_percent_change is None:
			print 'warning: no value found for percent change', symbol
			continue
			
		# we noticed that the percent change is often reported as a string like "+14.35%"...
		# let's get rid of the leading "+" and the trailing "%"
		if daily_percent_change.startswith('+'):
			# 'slice' the string (my_value[start_index:stop_index]); define the start index,
			# and in this case, no need to specify the end index
			daily_percent_change = daily_percent_change[1:]  
		
		# get rid of the trailing "%" 
		if daily_percent_change.endswith('%'):
			# 'slice' the string. this time, no need to define the start index, but definiely define the end index
			daily_percent_change = daily_percent_change[:-1]

		print symbol, daily_percent_change

		daily_percent_change_keyed_by_ticker_symbol[symbol] = daily_percent_change

	return daily_percent_change_keyed_by_ticker_symbol


class Command(BaseCommand):
    help = 'Updates the daily_percent_change for all Ticker objects'

    def handle(self, *args, **options):
		print 'starting script'

		event_log = DataHarvestEventLog()
		event_log.data_type = DATA_HARVEST_TYPE_MARKET_DATA
		event_log.notes = 'running'
		event_log.save()

		script_start_time = datetime.datetime.now()
		tickers = Ticker.objects.all().order_by('ticker_symbol')

		tickers_symbols_that_errored = set()
		count_tickers_successfully_updated = 0

		# let's process 25 tickers at a time. one implementation: use a for loop, where each loop
		# processes tickers of index x up to index x+25
		batch_size = 25
		start_idx = 0
		while start_idx < len(tickers):
			
			tickers_to_process = tickers[start_idx: start_idx+batch_size]

			symbols_as_list = ['\"'+t.ticker_symbol+'\"' for t in tickers_to_process]
			percent_changes_keyed_by_ticker_symbol = get_daily_percent_change(symbols_as_list)
			
			for ticker_to_process in tickers_to_process:
				try:
					ticker_to_process.daily_percent_change = percent_changes_keyed_by_ticker_symbol[ticker_to_process.ticker_symbol]
					ticker_to_process.save()
					count_tickers_successfully_updated += 1
				except Exception as e:
					print "couldn't set daily percent change", ticker_to_process.ticker_symbol, str(e)
					tickers_symbols_that_errored.add(ticker_to_process.ticker_symbol)

			start_idx += batch_size

		script_end_time = datetime.datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds
		notes = 'tickers updated: %d; ' % count_tickers_successfully_updated
		if tickers_symbols_that_errored:
			notes += 'errors: ' + ', '.join(tickers_symbols_that_errored)
		else:
			notes += 'no errors'
		event_log.notes = notes			
		event_log.save()

		print 'finished script'

		print 'tickers that errored: %d' % len(tickers_symbols_that_errored)
		print ', '.join(tickers_symbols_that_errored)