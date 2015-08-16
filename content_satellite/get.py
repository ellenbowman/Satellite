import urllib
import json
import datetime
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from django.conf import settings


def coverage():

	for t in Ticker.objects.all():

		promised_coverage_for_this_ticker = []

		if not t.services_for_ticker:
			continue
		if 'Stock Advisor' in t.services_for_ticker:
			print t.ticker_symbol, t.services_for_ticker
			promised_coverage_for_this_ticker.append('10% Promise (SA)')
			print promised_coverage_for_this_ticker
		if 'Rule Breakers' in t.services_for_ticker:
			print t.ticker_symbol, t.services_for_ticker
			promised_coverage_for_this_ticker.append('10% Promise (RB)')
			print promised_coverage_for_this_ticker
		else:
			pass

		t.promised_coverage = promised_coverage_for_this_ticker
		t.save()
		
		print t.promised_coverage