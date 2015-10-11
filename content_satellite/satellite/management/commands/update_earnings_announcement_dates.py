'''
update the 'earnings_announcement' field on all Ticker objects,
using expected earnings report dates retrieved from Quandl
'''
import urllib
import json
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_EARNINGS_DATES


def get_earnings_announcement_date(ticker_symbol):
	""" 
	get the 'EXP_RPT_DATE_QR1' (expected report date for 1st quarter?)
	from Quandl, which pulls from Zachs Research
	"""

	# sample url: http://www.quandl.com/api/v1/datasets/ZEA/AOL.json?column=4&auth_token=[quandl_auth_token]
	earnings_announcement_url = 'https://www.quandl.com/api/v1/datasets/ZEA/%s.json?column=4&auth_token=%s' % (ticker_symbol, settings.QUANDL_AUTH_TOKEN)

	earnings_response = urllib.urlopen(earnings_announcement_url).read()
	earnings_json = json.loads(earnings_response)

	# in the json that Quandl returns to us, the value representing the earnings date doesn't look like a typical date string. 
	# here's an example of what it looks like in the Quandl json: 20150427.0
	# these next two lines, we extract the value from the json and convert it into a conventional datetime type
	expected_report_date_quarter1 = str(int(earnings_json['data'][0][1]))
	earnings_announcement_date = datetime.datetime.strptime(expected_report_date_quarter1, '%Y%m%d')

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
			ticker_symbol = ticker.ticker_symbol
			try:
				earnings_announcement_date = get_earnings_announcement_date(ticker_symbol)
				print ticker_symbol, earnings_announcement_date
				ticker.earnings_announcement = earnings_announcement_date
				ticker.save()
			except Exception as e:
				ticker.earnings_announcement = "2099-01-01"
				ticker.save()
				print "couldn't set earnings date", ticker_symbol, str(e), ticker.earnings_announcement
				tickers_symbols_that_errored.add(ticker_symbol)

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