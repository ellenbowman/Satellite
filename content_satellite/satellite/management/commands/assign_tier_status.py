"Assigns coverage types to stocks depending on ticker, service, and tier status"

import urllib
import json
import datetime
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from django.conf import settings
import csv
from collections import defaultdict

class Command(BaseCommand):

    def handle(self, *args, **options):

	HIDDEN_GEMS_TIER_1 = ['HG']
	RULE_BREAKERS_TIER_1 = ['RB']
	STOCK_ADVISOR_TIER_1 = ['SA']

	TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME = {
	'Hidden Gems': HIDDEN_GEMS_TIER_1,
	'Rule Breakers': RULE_BREAKERS_TIER_1,
	'Stock Advisor': STOCK_ADVISOR_TIER_1,
	}

	for t in Ticker.objects.all():

		tier_status_for_this_ticker = []

		if t.services_for_ticker:
			service_pretty_names = t.services_for_ticker.split(',')
			for service_pretty_name in service_pretty_names:
				service_pretty_name = service_pretty_name.strip()
				if service_pretty_name in TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME:
						tier_status_for_this_ticker += TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME[service_pretty_name]


			# turn into a set in order to remove duplicates
			tier_status_for_this_ticker = set(tier_status_for_this_ticker)
			# turn back into a list, so that we can sort the values
			tier_status_for_this_ticker = list(tier_status_for_this_ticker)
			tier_status_for_this_ticker.sort()

			t.tier_status = ', '.join(tier_status_for_this_ticker)
			t.save()

		print t.ticker_symbol, t.tier_status