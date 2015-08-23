import urllib
import json
import datetime
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker
from django.conf import settings
import csv
from collections import defaultdict

def tiers():
	columns = defaultdict(list) # each value in each column is appended to a list

	with open('tiers.csv') as f:
		reader = csv.DictReader(f) # read rows into a dictionary format
		for row in reader: # read a row as {column1: value1, column2: value2,...}
			for (k,v) in row.items(): # go over each column name and value 
				columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

	tier_ones = (columns['ticker'])
	print tier_ones

	for t in Ticker.objects.all():
		if t.ticker_symbol in tier_ones:
			t.tier = 1
			print t.ticker_symbol, t.tier
			t.save()
			print t.ticker_symbol, t.tier, '---------'
		else:
			pass


def del_tiers():
	for t in Ticker.objects.all():
		if t.tier == 1:
			print t.ticker_symbol, t.tier
			zero = 0
			t.tier = zero
			t.save()
			print t.ticker_symbol, t.tier
		else:
			continue
	t.tier == 0
	t.save()


def tier():
	for t in Ticker.objects.all():
		tier_ones = ['BBBY', 'APOG', 'WGO', 'NKE', 'AVAV', 'CAMP', 'GBX', 'TCS', 'MSM', 'PEP', 'PSMT', 'SSW', 'JNJ', 'WFC', 'BLX', 'INTC',
		'BAC', 'KMI', 'NFLX', 'UNH', 'SHW', 'CTAS', 'GOOGL', 'GOOG', 'EBAY', 'PGR', 'ATHN', 'ALV', 'IBM', 'HAS', 'EDU', 'CNI', 'ILMN', 'HAL',
		'AAPL', 'ISRG', 'WSO', 'MANH', 'LLTC', 'FTI', 'TTS', 'CMG', 'AMTD', 'VZ', 'MSFT', 'IBKR', 'OMC', 'IRBT', 'GPRO', 'YHOO', 'KO', 'BABY',
		'QCOM', 'AXP', 'MKTX', 'ITW', 'CHKP', 'MSA', 'CLB', 'PLCM', 'PII', 'DLB', 'INFN', 'VMW', 'CRUS', 'NDAQ', 'PAC', 'CELG', 'BAX', 'TRIP',
		'MINI', 'IMAX', 'FAF', 'DLX', 'STAG', 'UL', 'TNC', 'UA', 'SBUX', 'NUE', 'FII', 'BJRI', 'V', 'KMB', 'GM', 'ALGN', 'RHI', 'DASTY', 'SRCL',
		'RSG', 'USLM', 'PRLB', 'P', 'NTGR', 'GNTX', 'CY', 'QLIK', 'N', 'AMZN', 'PACB', 'TRUE', 'FISI', 'WAB', 'STON', 'PEB', 'OII', 'SAVE',
		'QGEN', 'RPM', 'CMP', 'BIDU', 'SOHU', 'TWTR', 'CHRW', 'ULTI', 'SVU', 'PNRA', 'NATI', 'IPGP', 'CMI', 'AFL', 'NUVA', 'BOOM', 'RPXC', 'ESRX',
		'STO', 'PCAR', 'F', 'DORM', 'OAK', 'PCP', 'UPS', 'NSH', 'NOV', 'ASR', 'ARLP', 'GLW', 'YELP', 'BWLD', 'MSTR', 'XOOM', 'ORAN', 'SLAB',
		'RKUS', 'EQIX', 'FB', 'VRTX', 'NCR', 'MCK', 'MANT', 'MA', 'HY', 'CWT', 'WFM', 'SO', 'ANTM', 'SNCR', 'OTEX', 'GRMN', 'TOT', 'SCTY', 'MTH', 'CSGP',
		'LOCK', 'JLL', 'UGI', 'OGS', 'ATW', 'ROIC', 'CRI', 'STRZA', 'LFUS', 'FORM', 'EEFT', 'SSNC', 'WEC', 'TILE', 'SLCA', 'SBS', 'CMPR', 'NXPI', 'NOK',
		'SSYS', 'TEVA', 'SGEN', 'BMRN', 'ERJ', 'IRDM', 'ELLI', 'CHEF', 'LKQ', 'ITC', 'OCN', 'TEX', 'UPL', 'EPD', 'WPRT', 'GTLS', 'BOFI']
		if t.ticker_symbol in tier_ones:
			one = 1
			t.tier = one
			print t.ticker_symbol, t.tier
		else:
			continue
		t.save() 


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