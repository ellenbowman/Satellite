'''
update the 'daily_percent_change' field on all Ticker objects
'''
import urllib
import json
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker


def get_daily_percent_change(ticker_symbol):
	""" get the daily percent change, as reported by Yahoo Finance
	"""
	yahoo_finance_url = 'http://query.yahooapis.com/v1/public/yql'

	# when we make the request, pass along additional preferences, eg the SQL query
	data = {'q': "select Symbol, PercentChange from yahoo.finance.quotes where symbol='%s'" % ticker_symbol, 
	'format': 'json',
	'diagnostics':'false',
	'env': 'http://datatables.org/alltables.env',}

	encoded_data = urllib.urlencode(data)
	url = "%s?%s" % (yahoo_finance_url, encoded_data)

	yahoo_response = urllib.urlopen(url).read()
	yahoo_json = json.loads(yahoo_response)

	daily_percent_change = yahoo_json['query']['results']['quote']['PercentChange']  

	if daily_percent_change is None:
		print 'warning: no value found for percent change', ticker_symbol
		return None

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

	return daily_percent_change


class Command(BaseCommand):
    def handle(self, *args, **options):
		print 'starting script'

		script_start_time = datetime.datetime.now()
		tickers = Ticker.objects.all().order_by('ticker_symbol')

		tickers_symbols_that_errored = set()

		for ticker in tickers:
			ticker_symbol = ticker.ticker_symbol
			try:
				daily_percent_change = get_daily_percent_change(ticker_symbol)
				print ticker_symbol, daily_percent_change
				if daily_percent_change is not None:
					ticker.daily_percent_change = daily_percent_change
					ticker.save()
			except Exception as e:
				print "couldn't set daily percent change", ticker_symbol, str(e)
				tickers_symbols_that_errored.add(ticker_symbol)

		script_end_time = datetime.datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds
		print 'finished script'
		print 'tickers that errored: %d' % len(tickers_symbols_that_errored)
		print ', '.join(tickers_symbols_that_errored)