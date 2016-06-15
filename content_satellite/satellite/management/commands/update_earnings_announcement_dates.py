'''
update the 'earnings_announcement' field on all Ticker objects,
using expected earnings report dates retrieved from Moosie's API
'''
import urllib
import json
import datetime
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from requests.auth import HTTPBasicAuth
from satellite.models import Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_EARNINGS_DATES


def get_earnings_announcement_date(ticker_symbol):
	""" 
	get the next expected earnings date from Moosie's API at:
	https://fool.moosiefinance.com:8181/api/calendar/v1/company/ticker/{ticker1:ticker2}?pretty=1&canon=1
	"""

	earnings_announcement_url = 'https://fool.moosiefinance.com:8181/api/calendar/v1/company/ticker/%s' % ticker_symbol
	earnings_response = requests.get(earnings_announcement_url, auth=HTTPBasicAuth('calendar', 'aRfy!poo38;'), verify=False)
	earnings_response=earnings_response.json()
	earnings_announcement_date = earnings_response[ticker_symbol]['earnings_date']

	print earnings_announcement_date
	return earnings_announcement_date


class Command(BaseCommand):
    help = 'Updates the earnings_announcement for all Ticker objects'

    def handle(self, *args, **options):
		print 'starting script'

		event_log = DataHarvestEventLog()
		event_log.data_type = DATA_HARVEST_TYPE_EARNINGS_DATES
		event_log.notes = 'running'
		event_log.save()

		script_start_time = datetime.datetime.now()

		tickers_symbols_that_errored = set()
		tickers = Ticker.objects.all().order_by('ticker_symbol')
		for ticker in tickers:
			ticker.promised_coverage = None
			ticker_symbol = ticker.ticker_symbol
			if '-' in ticker_symbol:
				ticker_symbol = ticker_symbol.replace('-','.')
			print ticker_symbol
			try:
				earnings_announcement_date = get_earnings_announcement_date(ticker_symbol)
				print ticker_symbol, earnings_announcement_date
				ticker.earnings_announcement = earnings_announcement_date
				ticker.save()
			except Exception as e:
				ticker.earnings_announcement = '2099-01-01'
				ticker.save()
				print "couldn't set earnings date", ticker_symbol, str(e), ticker.earnings_announcement
				tickers_symbols_that_errored.add(ticker_symbol)
			if ticker.earnings_announcement == None:
				ticker.earnings_announcement = '2099-01-01'
				ticker.save()
			'below sets a text value for pending dates for display'
			if ticker.earnings_announcement == '2099-01-01':
				print ticker.promised_coverage
				ticker.promised_coverage = 'Earnings date pending'
				print ticker.promised_coverage
				ticker.save()
			else:
				continue


		script_end_time = datetime.datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds


		if tickers_symbols_that_errored:
			event_log.notes = 'errors: ' + ', '.join(tickers_symbols_that_errored)
		else:
			event_log.notes = 'no errors'
		event_log.save()


		print 'finished script'

		print 'tickers that errored: %d' % len(tickers_symbols_that_errored)
		print ', '.join(tickers_symbols_that_errored)		