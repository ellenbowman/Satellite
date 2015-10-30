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
    help = 'does nothing right now'

    def handle(self, *args, **options):
		print 'starting script'

		HIDDEN_GEMS_TIER_1 = ['HG Tier 1 Content']
		RULE_BREAKERS_TIER_1 = ['RB Tier 1 Content']
		STOCK_ADVISOR_TIER_1 = ['SA Tier 1 Content']


		# TIER_0_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME = {
		# 'Hidden Gems': HIDDEN_GEMS_TIER_0,
		# 'Rule Breakers': RULE_BREAKERS_TIER_0,
		# 'Stock Advisor': STOCK_ADVISOR_TIER_0,
		# }

		TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME = {
		'Hidden Gems': HIDDEN_GEMS_TIER_1,
		'Rule Breakers': RULE_BREAKERS_TIER_1,
		'Stock Advisor': STOCK_ADVISOR_TIER_1,
		}

		for t in Ticker.objects.all():

			promised_coverage_for_this_ticker = []

			if t.services_for_ticker:
				service_pretty_names = t.services_for_ticker.split(',')
				for service_pretty_name in service_pretty_names:
					service_pretty_name = service_pretty_name.strip()
					if service_pretty_name in TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME:
							promised_coverage_for_this_ticker += TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME[service_pretty_name]


				# turn into a set in order to remove duplicates
				promised_coverage_for_this_ticker = set(promised_coverage_for_this_ticker)
				# turn back into a list, so that we can sort the values
				promised_coverage_for_this_ticker = list(promised_coverage_for_this_ticker)
				promised_coverage_for_this_ticker.sort()

				t.promised_coverage = ', '.join(promised_coverage_for_this_ticker)
				t.save()

			print t.ticker_symbol, t.promised_coverage