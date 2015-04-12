# find additional data for each ticker - the percent change from a previous period (using yahoo finance), 
# get the earnings announcement (using Quandl.com), and get the number of scorecard followers (internal Leads API)

#Quandl auth key is SStNVWYv6_t4Q74MEooN

import urllib
import urllib2
import json
import datetime

from models import Ticker



def set_meta_data(quandl_auth_token, start_idx=None, batch_size=None):
	""" the 'public' function that we'll execute from the shell/admin """
	script_start_time = datetime.datetime.now()

	ticker_subset = Ticker.objects.all().order_by('ticker_symbol') 
	if start_idx is not None:
		ticker_subset = ticker_subset[start_idx:]
	if batch_size is not None:
		ticker_subset = ticker_subset[:batch_size]

	for ticker in ticker_subset:
		ticker_symbol = ticker.ticker_symbol

		print ticker_symbol


	# daily percent change ---------
		try:
			daily_percent_change = get_daily_percent_change(ticker_symbol)
			print daily_percent_change
			ticker.percent_change_historical = daily_percent_change
		except:
			print "couldn't set daily percent change"
		
		# performance ---------
		#try:
		#	percent_change_fifty_day_moving_average = get_historical_percent_change(ticker_symbol)
		#	print percent_change_fifty_day_moving_average
		#	ticker.percent_change_historical = percent_change_fifty_day_moving_average
		#except:
		#	print "couldn't set performance change"
	

		# date of next earnings announcement (estimate) ---------
		try:
			earnings_announcement_date = get_earnings_announcement_date(ticker_symbol, quandl_auth_token)
			print earnings_announcement_date
			ticker.earnings_announcement = earnings_announcement_date
		except:
			print "couldn't set earnings date"

		# scorecard followers ---------
		try:
			num_followers = get_num_scorecard_followers(ticker_symbol)
			print num_followers
			ticker.num_followers = num_followers
		except:
			print "couldn't set number of followers"

		# IMPORTANT!
		ticker.save()

	script_end_time = datetime.datetime.now()
	total_seconds = (script_end_time - script_start_time).total_seconds()
	print 'time elapsed: %d seconds' %  total_seconds	


# helper functions -- START ---

def get_historical_percent_change(ticker_symbol):
	""" get the percent change relative to the 50 day moving average, as reported by Yahoo Finance
	"""
	yahoo_finance_url = 'http://query.yahooapis.com/v1/public/yql'

	# when we make the request, pass along additional preferences, eg the SQL query
	data = {'q': "select Symbol, PercentChangeFromFiftydayMovingAverage from yahoo.finance.quotes where symbol='%s'" % ticker_symbol, 
	'format': 'json',
	'diagnostics':'false',
	'env': 'http://datatables.org/alltables.env',}

	encoded_data = urllib.urlencode(data)
	url = "%s?%s" % (yahoo_finance_url, encoded_data)

	yahoo_response = urllib.urlopen(url).read()
	yahoo_json = json.loads(yahoo_response)

	percent_change_moving_average = yahoo_json['query']['results']['quote']['PercentChangeFromFiftydayMovingAverage']  

	# we noticed that the percent change is often reported as a string like "+14.35%"...
	# let's get rid of the leading "+"/"-" and the trailing "%"
	if percent_change_moving_average.startswith('+') or percent_change_moving_average.startswith('-'):
		# 'slice' the string (my_value[start_index:stop_index]); define the start index, and in this case, no need to specify the end index
		percent_change_moving_average = percent_change_moving_average[1:]  
	
	# get rid of the trailing "%" 
	if percent_change_moving_average.endswith('%'):
		# 'slice' the string. this time, no need to define the start index, but definiely define the end index
		percent_change_moving_average = percent_change_moving_average[:-1]

	return percent_change_moving_average


def get_earnings_announcement_date(ticker_symbol, quandl_auth_token):
	""" get the 'EXP_RPT_DATE_QR1' (expected report date for 1st quarter?) 
	from Quandl, which pulls from Zachs Research
	Quandl auth key is SStNVWYv6_t4Q74MEooN"""

	# sample url: http://www.quandl.com/api/v1/datasets/ZEA/AOL.json?column=4&auth_token=[quandl_auth_token]
	earnings_announcement_url = 'http://www.quandl.com/api/v1/datasets/ZEA/%s.json?column=4&auth_token=%s' % (ticker_symbol, quandl_auth_token)
	
	earnings_response = urllib.urlopen(earnings_announcement_url).read()
	earnings_json = json.loads(earnings_response)

	expected_report_date_quarter1 = str(int(earnings_json['data'][0][1]))
	earnings_announcement_date = datetime.datetime.strptime(expected_report_date_quarter1, '%Y%m%d')

	return earnings_announcement_date
	

def get_num_scorecard_followers(ticker_symbol):
	""" returns the number of One members
	who follow this ticker in their Scorecard"""

	url='http://apiary.fool.com/leads/.json?serviceIds=1255&tickers=%s' % (ticker_symbol)
	#,1228,1008,1048,1066,1451,30,50,1069,52,18,1502&
	#,1228,1008,1048,1066,1451,30,50,1069,52,18,1502&tickers=%s' 
	# note: 1255 is Fool One, 1228 is Pro, 1008 is HG, 1048 is II, 1066 is IV, 1451 is DV,
	# 30 is MDP, 50 is Options, 1069 is RB, 52 is SpOps, 18 is SA, 1502 is SN
	lookie='Lookie=C6203A9167ABA57562DD83D6AEA13BCC1EDC892BE430D6915FA389C5437EDE6F4E8F70E752E1838A1C6343E400F5D8C230FB1395D04410E2049CA550A09989D258D66CC6C03D2201454FC58D4909FC982C45F62419E9EAFD323772179CB7C85F59970D042D2EB71BFD9F168B626BAA4A732E3E53A322D3CC4783BA8B56C6663A39BC100F'

	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', lookie.strip()))

	response = opener.open(url, timeout=10).read()
	json_response = json.loads(response)
	num_followers = json_response['SubscribersFollowingTicker']

	return num_followers

# helper functions -- END ---


'''
let's try to build a view where you can see the daily percentage change, latest articles and upcoming articles? 

'''


def get_daily_percent_change(ticker_symbol):
	""" get the daily percent change, as reported by Yahoo Finance
	At least, I assume it's daily. Just says 'percent change'
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

	# we noticed that the percent change is often reported as a string like "+14.35%"...
	# let's get rid of the leading "+"/"-" and the trailing "%"
	if daily_percent_change.startswith('+') or daily_percent_change.startswith('-'):
		# 'slice' the string (my_value[start_index:stop_index]); define the start index, and in this case, no need to specify the end index
		daily_percent_change = daily_percent_change[1:]  
	
	# get rid of the trailing "%" 
	if daily_percent_change.endswith('%'):
		# 'slice' the string. this time, no need to define the start index, but definiely define the end index
		daily_percent_change = daily_percent_change[:-1]

	return daily_percent_change

