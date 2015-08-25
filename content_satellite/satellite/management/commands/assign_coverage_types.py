"Assigns coverage types to stocks depending on ticker, service, and tier status"

import urllib
import json
import datetime
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from django.conf import settings
import csv
from collections import defaultdict

def coverage():

	#DEEP_VALUE = nothing
	HIDDEN_GEMS_TIER_0 = ['Fool.com Earnings (HG)']
	HIDDEN_GEMS_TIER_1 = ['Fool.com Earnings (HG)', 'Fool.com Earnings Preview (HG)']
	#II tier 0 = nothing
	INCOME_INVESTOR_TIER_1 = ['Fool.com Earnings (II)']
	INSIDE_VALUE_TIER_0 = ['Team Earnings (IV)', 'Fool.com Earnings (IV)']
	INSIDE_VALUE_TIER_1 = ['Team Earnings (IV)', 'Fool.com Earnings (IV)', 'Fool.com Earnings Preview (IV)']
	MDP_TIER_0 = ['Team Earnings (MDP)']
	# MDP: DVN, MSFT get earnings previews/reviews from Fool.com
	# MDP tier one: nothing
	ONE_TIER_0 = ['Fool.com Earnings (One)', 'Fool.com Earnings Preview (One)', 'Team Earnings (One)']
	OPTIONS_TIER_0 = ['Fool.com Earnings (Options)']
	#PRO = nothing
	RULE_BREAKERS_TIER_0 = ['10% Promise (RB)', 'Risk Ratings (RB)']
	RULE_BREAKERS_TIER_1 = ['10% Promise (RB)', 'Risk Ratings (RB)', 'Fool.com Earnings (RB)',
	'Fool.com Earnings Preview (RB)', 'Team Earnings (RB)', 'Potential 2-Minute Drill (RB)']
	#RYR = nothing
	SPECIAL_OPS_TIER_0 = ['Team Earnings (SpOps)']
	STOCK_ADVISOR_TIER_0 = ['10% Promise (SA)', 'Risk Ratings (SA)', 'Fool.com Earnings (SA)',
	'5 and 3 (SA)', '10% Potential (SA)']
	STOCK_ADVISOR_TIER_1 = ['10% Promise (SA)', 'Risk Ratings (SA)', 'Fool.com Earnings (SA)',
	'5 and 3 (SA)', '10% Potential (SA)', 'Fool.com Earnings Preview (SA)', 'Team Earnings (SA)',
	'Potential 2-Minute Drill (SA)']
	#SUPERNOVA: nothing


	TIER_0_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME = {
	'Hidden Gems': HIDDEN_GEMS_TIER_0,
	'Inside Value': INSIDE_VALUE_TIER_0,
	'MDP': MDP_TIER_0,
	'One': ONE_TIER_0,
	'Options': OPTIONS_TIER_0,
	'Rule Breakers': RULE_BREAKERS_TIER_0,
	'Stock Advisor': STOCK_ADVISOR_TIER_0,
	}

	TIER_1_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME = {
	'Hidden Gems': HIDDEN_GEMS_TIER_1,
	'Income Investor': INCOME_INVESTOR_TIER_1,
	'Inside Value': INSIDE_VALUE_TIER_1,
	'Rule Breakers': RULE_BREAKERS_TIER_1,
	'Stock Advisor': STOCK_ADVISOR_TIER_1,
	}

	for t in Ticker.objects.all():

		promised_coverage_for_this_ticker = []

		if t.services_for_ticker:
			service_pretty_names = t.services_for_ticker.split(',')
			for service_pretty_name in service_pretty_names:
				service_pretty_name = service_pretty_name.strip()
				if service_pretty_name in TIER_0_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME:
						print service_pretty_name
						promised_coverage_for_this_ticker += TIER_0_COVERAGE_KEYED_BY_SERVICE_PRETTY_NAME[service_pretty_name]
						print promised_coverage_for_this_ticker
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