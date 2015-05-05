'''
updates the BylineMetaData objects - account for authors of Articles published in the past year.
for each of those authors, compile the tickers and services they've covered in the past year.
'''
import urllib
import json
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Article, Service, BylineMetaData, DataHarvestEventLog, DATA_HARVEST_TYPE_BYLINE_META_DATA

def get_dictionaries_of_service_names_and_ticker_symbols_keyed_by_byline():
	service_names_set_keyed_by_author_name = {}
	ticker_symbols_set_keyed_by_author_name = {}

	one_year_ago = datetime(datetime.now().year-1, datetime.now().month, datetime.now().day)
	for art in Article.objects.filter(date_pub__gt=one_year_ago):
		byline = art.author

		if byline not in service_names_set_keyed_by_author_name:
			service_names_set_keyed_by_author_name[byline] = set()

		if byline not in ticker_symbols_set_keyed_by_author_name:
			ticker_symbols_set_keyed_by_author_name[byline] = set()

		service_names_set_keyed_by_author_name[byline].add(art.service.pretty_name)
		ticker_symbols_set_keyed_by_author_name[byline].add(art.ticker.ticker_symbol)

	print 'finished creating dictionaries. unique bylines:', len(service_names_set_keyed_by_author_name.keys())
	return service_names_set_keyed_by_author_name, ticker_symbols_set_keyed_by_author_name


class Command(BaseCommand):
    help = 'assigns the services_for_byline for all BylineMetaData objects'

    def handle(self, *args, **options):
		print 'starting script'

		event_log = DataHarvestEventLog()
		event_log.data_type = DATA_HARVEST_TYPE_BYLINE_META_DATA
		event_log.notes = 'running'
		event_log.save()

		script_start_time = datetime.now()

		notes = ''
		try:
			service_names_set_keyed_by_author_name, ticker_symbols_set_keyed_by_author_name = get_dictionaries_of_service_names_and_ticker_symbols_keyed_by_byline()

			for byline in service_names_set_keyed_by_author_name.keys():

				services_for_byline = service_names_set_keyed_by_author_name[byline]
				tickers_for_byline = ticker_symbols_set_keyed_by_author_name[byline]

				services_for_byline = list(services_for_byline)
				tickers_for_byline = list(tickers_for_byline)

				services_for_byline.sort()
				tickers_for_byline.sort()

				services_for_byline = ', '.join(services_for_byline)
				tickers_for_byline = ', '.join(tickers_for_byline)

				matches_by_byline = BylineMetaData.objects.filter(byline=byline)
				if matches_by_byline:
					for m in matches_by_byline:
						m.services = services_for_byline
						m.tickers = tickers_for_byline
						m.save()
				else:
					b = BylineMetaData()
					b.byline = byline
					b.services = services_for_byline
					b.tickers = tickers_for_byline
					b.save()


			for bylineMetaData in BylineMetaData.objects.all():
				if bylineMetaData.byline not in service_names_set_keyed_by_author_name.keys():
					bylineMetaData.services = "nothing in the last year"
					bylineMetaData.tickers = "nothing in the last year"
					bylineMetaData.save()
					continue

			notes = 'updated %d BylineMetaData objects' % len(service_names_set_keyed_by_author_name.keys())

		except Exception as e:
			print 'error', str(e)
			notes = "error: %s" % str(e)

		script_end_time = datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds
		event_log.notes = notes			
		event_log.save()

		print 'finished script'