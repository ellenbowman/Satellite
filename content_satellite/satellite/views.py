from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from forms import FilterForm, SelectAnalystForm
from models import Article, Service, Ticker, Scorecard, ServiceTake

# Create your views here.

###############################################################################

def index(request):
	context = {
		'page-title': 'Welcome to the Satellite',
	}

	tickers = Ticker.objects.all().order_by('daily_percent_change')
	gainer = tickers.reverse()[0]
	loser = tickers[0]
	latest = Article.objects.all().order_by('-date_pub')[0]

	dictionary_of_values = {
		'gainer': gainer,
		'loser': loser,
		'latest': latest,

	}

	return render(request, 'satellite/index.html', dictionary_of_values)

###############################################################################

def gainers_losers(list_of_tickers):
	tickers_sorted = sorted(list_of_tickers, key=lambda x: x.daily_percent_change, reverse = True)
	gainers = tickers_sorted[:10]
	losers = tickers_sorted[-10:]
	losers.reverse()

	return gainers, losers

###############################################################################

def tiered_stocks(request):

	tiered_stocks = []

	for t in Ticker.objects.all():
		if t.tier:
			tiered_stocks.append(t)
		else:
			print 'newp'

	services_to_filter_by = None 
	service_filter_description = None 
	tickers_to_filter_by = None
	ticker_filter_description = None
	service_options = Service.objects.all()
	tiers_to_filter_by = None
	tier_filter_description = None

	# filter by ticker/service/tier if we detect that preference in the query string (in the request.GET) or via a form post (in the request.POST)

	if request.POST:

		tiered_filter_form = FilterForm(request.POST)
		
		if tiered_filter_form.is_valid():

			if 'services' in tiered_filter_form.cleaned_data:
				if len(tiered_filter_form.cleaned_data['services']) > 0:
					services_to_filter_by = tiered_filter_form.cleaned_data['services']

			if 'tier_status' in tiered_filter_form.cleaned_data:
				tiers_user_input = tiered_filter_form.cleaned_data['tier_status']
				if len(tiers_user_input) > 0:
					tickers_to_filter_by = _get_ticker_objects_for_tier_status(tiers_user_input)
					print tickers_to_filter_by

		ticker_note_name_prefix = 'ticker_notes_'

		keys_of_ticker_note_data = [key_in_post_dict for key_in_post_dict in request.POST.keys() if key_in_post_dict.startswith(ticker_note_name_prefix)]

		for key_of_ticker_note_data in keys_of_ticker_note_data:

			ticker_id = key_of_ticker_note_data[len(ticker_note_name_prefix):]
			print ticker_id
			ticker_to_update = Ticker.objects.get(ticker_symbol=ticker_id) # ticker_id is a string, and ticker_symbol is an item from a list

			ticker_to_update.notes = request.POST[key_of_ticker_note_data] # retrieve from the POST dictionary the user input corresponding to this Ticker object
			ticker_to_update.save() # write this update to the db!
			
			print 'updated Ticker %s (id: %s). notes value: %s' % (ticker_to_update.ticker_symbol, ticker_id, ticker_to_update.notes)

	
	elif request.GET:
		initial_form_values = {}

		if 'tickers' in request.GET:
			tickers_user_input = request.GET.get('tickers')
			tickers_to_filter_by = _get_ticker_objects_for_ticker_symbols(tickers_user_input)
			initial_form_values['tickers'] = tickers_user_input
		if 'service_ids' in request.GET:
			services_to_filter_by = _get_service_objects_for_service_ids(request.GET.get('service_ids'))
			initial_form_values['services'] = services_to_filter_by
		if 'tier_status' in request.GET:
			tiers_user_input = request.GET.get('tier_status')
			tiers_to_filter_by = _get_ticker_objects_for_tier_status(tiers_user_input)
			initial_form_values['tier_status'] = tiers_to_filter_by
			print tiers_user_input

		tiered_filter_form = FilterForm(initial=initial_form_values)

	else:
		tiered_filter_form = FilterForm()

	# end of inspecting request.GET and request.POST for ticker/service/tier filter


	if services_to_filter_by:
		# make the pretty description of the services we found. 
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)

	if tickers_to_filter_by:
		tier_status_names = [t.tier_status for t in tickers_to_filter_by]
		tier_status_names.sort()
		tier_status_names = set(tier_status_names)
		tier_filter_description = ', '.join(tier_status_names)

	else:
		pass


	# If there's a service filter, and a tier filter: Get the objects that match all two.
	if tickers_to_filter_by is not None and services_to_filter_by is not None:
		tiered_stocks = []
		for t in tickers_to_filter_by:
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker and t.tier is not 0:
					tiered_stocks.append(t)  # add tickers one by one, if the ticker and the service match the filter
					# and a tier exists
					break

	elif services_to_filter_by is not None:
		tiered_stocks = []  # initialize to an empty list
		for t in Ticker.objects.all():
			if t.services_for_ticker is None:
				continue
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker and t.tier is not 0:
					tiered_stocks.append(t)  # add tickers one by one, if the ticker and the service match the filter
				# and a tier exists
				break

	elif tickers_to_filter_by is not None:
		tiered_stocks = tickers_to_filter_by
		
	else:
		# get all tiered stocks
		tiered_stocks = []
		for t in Ticker.objects.all():
			if t.tier_status:
				tiered_stocks.append(t)


	dictionary_of_values = {
		'tiered_stocks': tiered_stocks,
		'tiered_filter_form': FilterForm,
		'ticker_filter_description': ticker_filter_description,
		'service_filter_description': service_filter_description,
		'tier_filter_description': tier_filter_description,
	}

	return render(request, 'satellite/tiered_stocks.html', dictionary_of_values)



###############################################################################

def upcoming_earnings(list_of_tickers):
	yesterday = (datetime.now() - timedelta(days=1)).date()  # a date object that represents yesterday's date. we'll then consider only the tickers whose earnings announcement are greater than this value.
	earnings = [t for t in list_of_tickers if t.earnings_announcement is not None and t.earnings_announcement > yesterday]
	earnings = sorted(earnings, key=lambda x: x.earnings_announcement)[:10]

	return earnings

###############################################################################

def recent_articles(list_of_articles):
	duplicate_titles = set()
	individual_articles = []
	for a in list_of_articles:
		if a.title not in duplicate_titles:
			individual_articles.append(a)
			duplicate_titles.add(a.title)
	articles = sorted(individual_articles, key=lambda x: x.date_pub, reverse=True)[:5]

	return articles

###############################################################################

def service_overview(request):

	fool_one_tickers = []
	supernova_tickers = []
	pro_tickers = []
	mdp_tickers = []
	stock_advisor_tickers = []
	hidden_gems_tickers = []
	income_investor_tickers = []
	rule_breakers_tickers = []
	inside_value_tickers = []
	special_ops_tickers = []
	deep_value_tickers = []
	options_tickers = []

	for t in Ticker.objects.all():
		if not t.services_for_ticker:
			continue
		was_processed = False    
		if 'One' in t.services_for_ticker:
			fool_one_tickers.append(t)
			was_processed = True
		if 'Supernova' in t.services_for_ticker:
			supernova_tickers.append(t)
			was_processed = True
		if 'Pro' in t.services_for_ticker:
			pro_tickers.append(t)
			was_processed = True
		if 'MDP' in t.services_for_ticker:
			mdp_tickers.append(t)
			was_processed = True
		if 'Stock Advisor' in t.services_for_ticker:
			stock_advisor_tickers.append(t)
			was_processed = True
		if 'Hidden Gems' in t.services_for_ticker:
			hidden_gems_tickers.append(t)
			was_processed = True
		if 'Income Investor' in t.services_for_ticker:
			income_investor_tickers.append(t)
			was_processed = True
		if 'Rule Breakers' in t.services_for_ticker:
			rule_breakers_tickers.append(t)
			was_processed = True
		if 'Inside Value' in t.services_for_ticker:
			inside_value_tickers.append(t)
			was_processed = True
		if 'Special Ops' in t.services_for_ticker:
			special_ops_tickers.append(t)
			was_processed = True
		if 'Options' in t.services_for_ticker:
			options_tickers.append(t)
			was_processed = True
		if 'Deep Value' in t.services_for_ticker:
			deep_value_tickers.append(t)
			was_processed = True
		if was_processed == False:
			print 'this ticker %s was in some other service' % t.ticker_symbol


	fool_one_articles = []
	supernova_articles = []
	pro_articles = []
	mdp_articles = []
	stock_advisor_articles = []
	hidden_gems_articles = []
	income_investor_articles = []
	rule_breakers_articles = []
	inside_value_articles = []
	special_ops_articles = []
	deep_value_articles = []
	options_articles = []

	for a in Article.objects.filter(date_pub__gt = (datetime.now() - timedelta(days=21)).date()):    
		if 'One' in a.service.pretty_name:
			fool_one_articles.append(a)
		elif 'Supernova' in a.service.pretty_name:
			supernova_articles.append(a)
		elif 'Pro' in a.service.pretty_name:
			pro_articles.append(a)
		elif 'MDP' in a.service.pretty_name:
			mdp_articles.append(a)
		elif 'Stock Advisor' in a.service.pretty_name:
			stock_advisor_articles.append(a)
		elif 'Hidden Gems' in a.service.pretty_name:
			hidden_gems_articles.append(a)
		elif 'Income Investor' in a.service.pretty_name:
			income_investor_articles.append(a)
		elif 'Rule Breakers' in a.service.pretty_name:
			rule_breakers_articles.append(a)
		elif 'Inside Value' in a.service.pretty_name:
			inside_value_articles.append(a)
		elif 'Special Ops' in a.service.pretty_name:
			special_ops_articles.append(a)
		elif 'Options' in a.service.pretty_name:
			options_articles.append(a)
		elif 'Deep Value' in a.service.pretty_name:
			deep_value_articles.append(a)
		else:
			print 'this article was in some other service'


	yesterday = (datetime.now() - timedelta(days=1)).date()  # a date object that represents yesterday's date. we'll then consider only the tickers whose earnings announcement are greater than this value.


	fool_one_gainers, fool_one_losers = gainers_losers(fool_one_tickers)
	fool_one_earnings = upcoming_earnings(fool_one_tickers)
	fool_one_articles = recent_articles(fool_one_articles)

	supernova_gainers, supernova_losers = gainers_losers(supernova_tickers)
	supernova_earnings = upcoming_earnings(supernova_tickers)
	supernova_articles = recent_articles(supernova_articles)
        
	pro_gainers, pro_losers = gainers_losers(pro_tickers)
	pro_earnings = upcoming_earnings(pro_tickers)
	pro_articles = recent_articles(pro_articles)

	mdp_gainers, mdp_losers = gainers_losers(mdp_tickers)
	mdp_earnings = upcoming_earnings(mdp_tickers)
	mdp_articles = recent_articles(mdp_articles)

	stock_advisor_gainers, stock_advisor_losers = gainers_losers(stock_advisor_tickers)
	stock_advisor_earnings = upcoming_earnings(stock_advisor_tickers)
	stock_advisor_articles = recent_articles(stock_advisor_articles)

	rule_breakers_gainers, rule_breakers_losers = gainers_losers(rule_breakers_tickers)
	rule_breakers_earnings = upcoming_earnings(rule_breakers_tickers)
	rule_breakers_articles = recent_articles(rule_breakers_articles)

	income_investor_gainers, income_investor_losers = gainers_losers(income_investor_tickers)
	income_investor_earnings = upcoming_earnings(income_investor_tickers)
	income_investor_articles = recent_articles(income_investor_articles)

	inside_value_gainers, inside_value_losers = gainers_losers(inside_value_tickers)
	inside_value_earnings = upcoming_earnings(inside_value_tickers)
	inside_value_articles = recent_articles(inside_value_articles)

	hidden_gems_gainers, hidden_gems_losers = gainers_losers(hidden_gems_tickers)
	hidden_gems_earnings = upcoming_earnings(hidden_gems_tickers)
	hidden_gems_articles = recent_articles(hidden_gems_articles)

	special_ops_gainers, special_ops_losers = gainers_losers(special_ops_tickers)
	special_ops_earnings = upcoming_earnings(special_ops_tickers)
	special_ops_articles = recent_articles(special_ops_articles)

	# options_gainers, options_losers = gainers_losers(options_tickers)
	# options_earnings = sorted(options_tickers, key=lambda x: x.earnings_announcement, reverse=True)[:10]
	options_articles = recent_articles(options_articles)

	deep_value_gainers, deep_value_losers = gainers_losers(deep_value_tickers)
	deep_value_earnings = upcoming_earnings(deep_value_tickers)
	deep_value_articles = recent_articles(deep_value_articles)


	dictionary_of_values = {
		'fool_one_tickers': fool_one_tickers,
		'fool_one_gainers': fool_one_gainers,
		'fool_one_losers': fool_one_losers,
		'fool_one_earnings': fool_one_earnings,
		'fool_one_articles': fool_one_articles,
		'supernova_tickers': supernova_tickers,
		'supernova_gainers': supernova_gainers,
		'supernova_losers': supernova_losers,
		'supernova_earnings': supernova_earnings,
		'supernova_articles': supernova_articles,
		'pro_tickers': pro_tickers,
		'pro_gainers': pro_gainers,
		'pro_losers': pro_losers,
		'pro_earnings': pro_earnings,
		'pro_articles': pro_articles,
		'mdp_tickers': mdp_tickers,
		'mdp_gainers': mdp_gainers,
		'mdp_losers': mdp_losers,
		'mdp_earnings': mdp_earnings,
		'mdp_articles': mdp_articles,
		'stock_advisor_tickers': stock_advisor_tickers,
		'stock_advisor_gainers': stock_advisor_gainers,
		'stock_advisor_losers': stock_advisor_losers,
		'stock_advisor_earnings': stock_advisor_earnings,
		'stock_advisor_articles': stock_advisor_articles,
		'rule_breakers_tickers': rule_breakers_tickers,
		'rule_breakers_gainers': rule_breakers_gainers,
		'rule_breakers_losers': rule_breakers_losers,
		'rule_breakers_earnings': rule_breakers_earnings,
		'rule_breakers_articles': rule_breakers_articles,
		'income_investor_tickers': income_investor_tickers,
		'income_investor_gainers': income_investor_gainers,
		'income_investor_losers': income_investor_losers,
		'income_investor_earnings': income_investor_earnings,
		'income_investor_articles': income_investor_articles,
		'inside_value_tickers': inside_value_tickers,
		'inside_value_gainers': inside_value_gainers,
		'inside_value_losers': inside_value_losers,
		'inside_value_earnings': inside_value_earnings,
		'inside_value_articles': inside_value_articles,
		'hidden_gems_tickers': hidden_gems_tickers,
		'hidden_gems_gainers': hidden_gems_gainers,
		'hidden_gems_losers': hidden_gems_losers,
		'hidden_gems_earnings': hidden_gems_earnings,
		'hidden_gems_articles': hidden_gems_articles,
		'special_ops_tickers': special_ops_tickers,
		'special_ops_gainers': special_ops_gainers,
		'special_ops_losers': special_ops_losers,
		'special_ops_earnings': special_ops_earnings,
		'special_ops_articles': special_ops_articles,
		'deep_value_tickers': deep_value_tickers,
		'deep_value_gainers': deep_value_gainers,
		'deep_value_losers': deep_value_losers,
		'deep_value_earnings': deep_value_earnings,
		'deep_value_articles': deep_value_articles,
		#'options_tickers': options_tickers,
		#'options_gainers': options_gainers,
		#'options_losers': options_losers,
		#'options_earnings': options_earnings,
		'options_articles': options_articles,

	}

	return render(request, 'satellite/service_overview.html', dictionary_of_values)


###############################################################################


def movers(request):
	# here we practice using 'context'
	context = {
		'pagetitle': "Today's Biggest Movers",
		'tickers': Ticker.objects.all().order_by('ticker_symbol')[:20],
		'scorecards': Scorecard.objects.all().order_by('pretty_name'),
		'biggestmovers': Ticker.objects.all().order_by('-daily_percent_change')[:20],
	}

	return render(request, 'satellite/movers.html', context)


###############################################################################

def articles_by_service(request):
	
	""
	service_name = None
	if 'service' in request.GET:
		service_name = request.GET['service']

	max_count = 20

	if service_name:
		service_match = Service.objects.filter(name=service_name)
		articles = Article.objects.filter(service__in=service_match)[:max_count]
	else:
		articles = Article.objects.all()[:max_count]

	dictionary_of_values = {
		'articles' : articles,
		'service_name': service_name,
		'articles_max_count': max_count
	}

	return render(request, 'satellite/articles_by_service.html', dictionary_of_values)


###############################################################################

def _get_ticker_objects_for_ticker_symbols(ticker_symbols_csv='AAPL,SWIR,Z'):
	csv_elements = ticker_symbols_csv.split(',')
	csv_elements = [el.strip().upper() for el in csv_elements]

	return Ticker.objects.filter(ticker_symbol__in=csv_elements)

def _get_service_objects_for_service_ids(service_ids_csv='1,4,7'):
	csv_elements = service_ids_csv.split(',')
	csv_elements = [int(el.strip()) for el in csv_elements]
	return Service.objects.filter(id__in=csv_elements)

def _get_ticker_objects_for_tier_status(tier_status_csv=['core','first']):
	# given a set of tier statuses, find corresponding ticker objects
	csv_elements = tier_status_csv
	print csv_elements

	return Ticker.objects.filter(tier_status__in=csv_elements)

###############################################################################

def ticker_world(request, sort_by='daily_percent_change'):

	#shows all tickers and some meta data (daily percent change, company name, exchange, ticker symbol)
	#contains a form that lets you specify services and tickers
	#if a service or ticker's name is detected in the request's POST dictionary, then filters to tickers for that service or ticker

	services_to_filter_by = None 	# will hold the Service objects that satisfy our filter
	service_filter_description = None   # this will be a string description of the service filter. we'll display this value on the page.
	tickers_to_filter_by = None
	ticker_filter_description = None
	service_options = Service.objects.all()

	# filter by ticker/service if we detect that preference in the query string (in the request.GET) or via a form post (in the request.POST)
	# additionally, if this is a GET, let's attempt to set the page_num. otherwise, we'll default to page_num of 1.

	if request.POST:
		if 'page_number' in request.POST:
			page_num = int(request.POST['page_number'])

		movers_filter_form = FilterForm(request.POST)
		
		if movers_filter_form.is_valid():
			if 'tickers' in movers_filter_form.cleaned_data:
				tickers_user_input = movers_filter_form.cleaned_data['tickers'].strip()
				if tickers_user_input != '':
					# take the user input and try to find corresponding Ticker objects 
					tickers_to_filter_by = _get_ticker_objects_for_ticker_symbols(tickers_user_input)

			# retrieve the services that were selected in the form. 
			if 'services' in movers_filter_form.cleaned_data:
				if len(movers_filter_form.cleaned_data['services']) > 0:
					# the form makes available "cleaned data" that's pretty convenient - 
					# in this case, it returns a list of Service objects that correspond
					# to what the user selected.
					services_to_filter_by = movers_filter_form.cleaned_data['services']

		
		# find the keys that correspond to the 'notes' input. 
		# since we also have control over the forms markup (embedded in 'info_by_scorecard.html'), 
		# we know that the form data we're interested in has names that start with 'ticker_notes_'.
		# it translates that these names should be visible as keys in the request.POST dictionary

		ticker_note_name_prefix = 'ticker_notes_'

		# use 'python list comprehension' to create a list of all the keys in request.POST that 
		# match this condition: the key must start with 'ticker_notes_' . equivalent to a multi-line
		# 'for' loop.
		keys_of_ticker_note_data = [key_in_post_dict for key_in_post_dict in request.POST.keys() if key_in_post_dict.startswith(ticker_note_name_prefix)]

		for key_of_ticker_note_data in keys_of_ticker_note_data:
			# from each key, we can extract the Ticker id that we've embedded in the key
			# (eg, if we see 'ticker_notes_3', we know it corresponds to the Ticker with id 3)
			# and we can use that id to retrieve the Ticker object from the db,
			# update its notes field, and save the Ticker. voila!

			ticker_id = key_of_ticker_note_data[len(ticker_note_name_prefix):]  # pick out everything in the string that follows the 'ticker_notes_' prefix
			print ticker_id
			ticker_to_update = Ticker.objects.get(ticker_symbol=ticker_id) # ticker_id is a string, and ticker_symbol is an item from a list

			ticker_to_update.notes = request.POST[key_of_ticker_note_data] # retrieve from the POST dictionary the user input corresponding to this Ticker object
			ticker_to_update.save() # write this update to the db!
			
			# print to console a sanity check
			print 'updated Ticker %s (id: %s). notes value: %s' % (ticker_to_update.ticker_symbol, ticker_id, ticker_to_update.notes)

	
	elif request.GET:
		initial_form_values = {}

		if 'tickers' in request.GET:
			tickers_user_input = request.GET.get('tickers')
			tickers_to_filter_by = _get_ticker_objects_for_ticker_symbols(tickers_user_input)

			initial_form_values['tickers'] = tickers_user_input
		if 'service_ids' in request.GET:
			services_to_filter_by = _get_service_objects_for_service_ids(request.GET.get('service_ids'))
			initial_form_values['services'] = services_to_filter_by

		movers_filter_form = FilterForm(initial=initial_form_values)

	else:
		movers_filter_form = FilterForm()

	# end of inspecting request.GET and request.POST for ticker/service filter

	if tickers_to_filter_by:
		# make the pretty description of the tickers
		ticker_filter_description = tickers_user_input.upper()

	if services_to_filter_by:
		# make the pretty description of the services we found. 
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)

	else:
		pass


	# get the set of tickers, filtered by ticker/service, if those filters are defined
	if tickers_to_filter_by is not None and services_to_filter_by is not None:
		tickers = []  # initialize to an empty list
		for t in tickers_to_filter_by:
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker:
					tickers.append(t)  # one-by-one we'll add tickers, pending checks on whether there's 
					# overlap between the ticker's services_for_ticker field and the set of services we 
					# want to filter by 
					break
		
	elif tickers_to_filter_by is not None:
		tickers = tickers_to_filter_by
	elif services_to_filter_by is not None:
		tickers = []  # initialize to an empty list
		for t in Ticker.objects.all():
			if not t.services_for_ticker:
				continue
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker:
					tickers.append(t)  # one-by-one we'll add tickers, pending checks on whether there's 
					# overlap between the ticker's services_for_ticker field and the set of services we 
					# want to filter by 
					break
		
	else:
		# get all tickers, and sort by descending date
		tickers = Ticker.objects.all()
	

	yesterday = (datetime.now() - timedelta(days=1)).date()  # a date object that represents yesterday's date. we'll then consider only the tickers whose earnings announcement are greater than this value.

	if sort_by=='daily_percent_change':
		tickers = sorted(tickers, key=lambda x: x.daily_percent_change, reverse=True)
		top_gainers = tickers[:10]
		top_losers = tickers[::-1][:10]

	else:
		tickers_without_announcement_date = []
		tickers_with_announcement_date_and_in_past = []
		tickers_with_announcement_date_and_not_in_past = []

		for t in tickers:
			if t.earnings_announcement:
				if t.earnings_announcement > yesterday:
					tickers_with_announcement_date_and_not_in_past.append(t)
				else:
					tickers_with_announcement_date_and_in_past.append(t)
			else:
				tickers_without_announcement_date.append(t)

		tickers = sorted(tickers_with_announcement_date_and_not_in_past, key=lambda x: x.earnings_announcement) + tickers_without_announcement_date + sorted(tickers_with_announcement_date_and_in_past, key=lambda x: x.earnings_announcement) 
		top_gainers = sorted(tickers, key=lambda x: x.daily_percent_change, reverse=True)[:10]
		top_losers = sorted(tickers, key=lambda x: x.daily_percent_change)[:10]
		loser = tickers[0]
		print loser

	if sort_by == 'biggest_losers':
		tickers = sorted(tickers, key=lambda x: x.daily_percent_change)

	if sort_by == 'all_tickers':
		tickers = sorted(tickers, key=lambda x: x.company_name)

	num_tickers = len(tickers)

	# tickers_sorted_by_earnings_date = tickers.order_by('earnings_announcement')[:10]
	# let's consider only those that are happening today or in the future

	tickers_sorted_by_earnings_date = [t for t in tickers if t.earnings_announcement != None and t.earnings_announcement>yesterday]
	tickers_sorted_by_earnings_date = sorted(tickers_sorted_by_earnings_date, key=lambda x: x.earnings_announcement)[:10]

	next_week_date = (datetime.now() + timedelta(days=7)).date()

	#if next_week=='next_week':
	#	tickers_for_next_week = [t for t in tickers if t.earnings_announcement != None and t.earnings_announcement<next_week_date and t.earnings_announcement>yesterday]
	#	tickers_for_next_week = sorted(tickers_for_next_week, key=lambda x: x.earnings_announcement)
	#else:
	#	tickers_for_next_week = None

	dictionary_of_values = {
		'form': movers_filter_form,
		'tickers': tickers,
		'num_tickers' : num_tickers,
		'service_filter_description': service_filter_description,
		'ticker_filter_description': ticker_filter_description,
		'services_to_filter_by': services_to_filter_by,
		'tickers_to_filter_by': tickers_to_filter_by,
		'service_options': service_options,
		'top_gainers': top_gainers,
		'top_losers': top_losers,
		'tickers_sorted_by_earnings_date': tickers_sorted_by_earnings_date,
		#'next_week_date': next_week_date,
		#'next_week': next_week,
		#'tickers_for_next_week': tickers_for_next_week,
		# 'ticker_filter_description': ticker_filter_description
	}

	if sort_by=='daily_percent_change':
		dictionary_of_values['sort_by_daily_percent_change'] = True

	if sort_by=='biggest_losers':
		dictionary_of_values['sort_by_biggest_losers'] = True

	if sort_by=='all_tickers':
		dictionary_of_values['sort_by_all_tickers'] = True

	return render(request, 'satellite/ticker_world.html', dictionary_of_values)


###############################################################################

def content_audit(request):

	services_to_filter_by = None 	# will hold the Service objects that satisfy our filter
	service_filter_description = None   # this will be a string description of the service filter. we'll display this value on the page.
	service_options = Service.objects.all()


	if request.POST:

		analyst_form = SelectAnalystForm(request.POST)
		#if analyst_form.is_valid():
			#analyst_form.save(commit=True)
			#return "http://satellite.fool.com/sol/content_audit/"

		audit_filter_form = FilterForm(request.POST)
		
		if audit_filter_form.is_valid(): 
			if 'services' in audit_filter_form.cleaned_data:
				if len(audit_filter_form.cleaned_data['services']) > 0:
					services_to_filter_by = audit_filter_form.cleaned_data['services']

		ticker_note_name_prefix = 'ticker_notes_'
		keys_of_ticker_note_data = [key_in_post_dict for key_in_post_dict in request.POST.keys() if key_in_post_dict.startswith(ticker_note_name_prefix)]

		for key_of_ticker_note_data in keys_of_ticker_note_data:
			ticker_id = key_of_ticker_note_data[len(ticker_note_name_prefix):]  # pick out everything in the string that follows the 'ticker_notes_' prefix
			print ticker_id
			ticker_to_update = Ticker.objects.get(ticker_symbol=ticker_id) # ticker_id is a string, and ticker_symbol is an item from a list

			ticker_to_update.notes = request.POST[key_of_ticker_note_data] # retrieve from the POST dictionary the user input corresponding to this Ticker object
			ticker_to_update.save() # write this update to the db!
			
			# print to console a sanity check
			print 'updated Ticker %s (id: %s). notes value: %s' % (ticker_to_update.ticker_symbol, ticker_id, ticker_to_update.notes)

	
	elif request.GET:

		analyst_form = SelectAnalystForm()

		initial_form_values = {}
		if 'service_ids' in request.GET:
			services_to_filter_by = _get_service_objects_for_service_ids(request.GET.get('service_ids'))
			initial_form_values['services'] = services_to_filter_by

		audit_filter_form = FilterForm(initial=initial_form_values)

	else:
		audit_filter_form = FilterForm()
		analyst_form = SelectAnalystForm()

	if services_to_filter_by:
		# make the pretty description of the services we found. 
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)
	else:
		pass


	# get the set of tickers, filtered by service
	if services_to_filter_by is not None:
		tickers = []
		for t in Ticker.objects.all():
			for service in services_to_filter_by:
				if t.services_for_ticker is None:
					pass
				elif service.pretty_name in t.services_for_ticker:
					tickers.append(t)
				break

		#print tickers

		#articles = 'pants'

		filtered_articles = []
		for a in Article.objects.all():
			for t in tickers:
				if a.service.pretty_name in t.services_for_ticker:
					filtered_articles.append(a)
				else:
					pass
		#print filtered_articles

		duplicate_titles = set()
		individual_articles = []
		for a in filtered_articles:
			if a.title not in duplicate_titles:
				duplicate_titles.add(a.title)
				individual_articles.append(a)

		print individual_articles[:5]


	else:
		# get all tickers, and sort by descending date
		tickers = Ticker.objects.all()
		individual_articles = 'pants'


	dictionary_of_values = {
		'tickers': tickers,
		'individual_articles': individual_articles,
		'form': audit_filter_form,
		'analyst_form': analyst_form,
		'service_filter_description': service_filter_description,
	}

	return render(request, 'satellite/content_audit.html', dictionary_of_values)




###############################################################################


def scorecard_index(request):
	"""
	a listing of the scorecards, ordered by pretty name
	"""

	all_scorecards = Scorecard.objects.all().order_by('pretty_name')

	dictionary_of_values = {
		'scorecards_in_alpha_order' : all_scorecards,
	}

	return render(request, 'satellite/scorecard_index.html', dictionary_of_values)

###############################################################################