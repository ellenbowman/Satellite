'''
zero-out the 'daily_percent_change' field on all Ticker objects
'''
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_MARKET_DATA



class Command(BaseCommand):
    help = 'zero-out the daily_percent_change for all Ticker objects'

    def handle(self, *args, **options):
		print 'starting script'

		event_log = DataHarvestEventLog()
		event_log.data_type = DATA_HARVEST_TYPE_MARKET_DATA
		event_log.notes = 'running'
		event_log.save()

		tickers_symbols_that_errored = set()
		count_tickers_successfully_updated = 0

		script_start_time = datetime.now()
		
		for ticker in Ticker.objects.all():
			try:
				ticker.daily_percent_change = 0
				ticker.save()
				count_tickers_successfully_updated += 1
			except Exception as e:
				print "couldn't reset daily percent change", ticker.ticker_symbol, str(e)
				tickers_symbols_that_errored.add(ticker.ticker_symbol)


		script_end_time = datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds
		notes = 'tickers reset: %d; ' % count_tickers_successfully_updated
		if tickers_symbols_that_errored:
			notes += 'errors: ' + ', '.join(tickers_symbols_that_errored)
		else:
			notes += 'no errors'
		event_log.notes = notes			
		event_log.save()

		print 'finished script'

		print 'tickers that errored: %d' % len(tickers_symbols_that_errored)
		print ', '.join(tickers_symbols_that_errored)