from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from forms import FilterForm
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
	articles = Article.objects.all().order_by('date_pub')
	latest = articles.reverse()[0]
	print latest

	upcoming_earnings = Ticker.objects.all().order_by('earnings_announcement')[:5]
	print upcoming_earnings

	dictionary_of_values = {
		'gainer': gainer,
		'loser': loser,
		'latest': latest,
	}

	return render(request, 'satellite/index.html', dictionary_of_values)

###############################################################################


def service_overview(request):

	services_to_filter_by = None 	# will hold the Service objects that satisfy our filter
	service_filter_description = None   # this will be a string description of the service filter. we'll display this value on the page.
	service_options = Service.objects.all()

	# filter by service if we detect that preference in the query string (in the request.GET) or via a form post (in the request.POST)

	if request.POST:

		service_filter_form = FilterForm(request.POST)
		
		if service_filter_form.is_valid():
			# retrieve the services that were selected in the form. 
			if 'services' in service_filter_form.cleaned_data:
				if len(service_filter_form.cleaned_data['services']) > 0:
					# the form makes available "cleaned data" that's pretty convenient - 
					# in this case, it returns a list of Service objects that correspond
					# to what the user selected.
					services_to_filter_by = service_filter_form.cleaned_data['services']

	
	elif request.GET:
		initial_form_values = {}

		if 'service_ids' in request.GET:
			services_to_filter_by = _get_service_objects_for_service_ids(request.GET.get('service_ids'))
			initial_form_values['services'] = services_to_filter_by

		service_filter_form = FilterForm(initial=initial_form_values)

	else:
		service_filter_form = FilterForm()

	# end of inspecting request.GET and request.POST for ticker/service filter

	if services_to_filter_by:
		# make the pretty description of the services we found. 
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)

	else:
		pass


	# get the set of tickers, filtered by service, if that filter is defined
	if services_to_filter_by is not None:
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

	fool_one_tickers = []
	supernova_tickers = []
	pro_tickers = []
	for t in Ticker.objects.all():
		if not t.services_for_ticker:
			continue
            
		if 'One' in t.services_for_ticker:
			fool_one_tickers.append(t)
		elif 'Supernova' in t.services_for_ticker:
			supernova_tickers.append(t)
		elif 'Pro' in t.services_for_ticker:
			pro_tickers.append(t)
		else:
			print 'this ticker %s was in a service other than One, Supernova, or Pro' % t.ticker_symbol
    
	fool_one_gainers = sorted(fool_one_tickers, key=lambda x: x.daily_percent_change, reverse=True)[:5]
	fool_one_losers = sorted(fool_one_tickers, key=lambda x: x.daily_percent_change)[:5]

	supernova_gainers = sorted(supernova_tickers, key=lambda x: x.daily_percent_change, reverse=True)[:5]
	supernova_losers = sorted(supernova_tickers, key=lambda x: x.daily_percent_change)[:5]
        
	pro_gainers = sorted(pro_tickers, key=lambda x: x.daily_percent_change, reverse=True)[:5]
	pro_losers = sorted(pro_tickers, key=lambda x: x.daily_percent_change)[:5]


	dictionary_of_values = {
		'services_to_filter_by': services_to_filter_by,
		'tickers': tickers,
		'form': service_filter_form,
		'fool_one_tickers': fool_one_tickers,
		'fool_one_gainers': fool_one_gainers,
		'fool_one_losers': fool_one_losers,
		'supernova_tickers': supernova_tickers,
		'supernova_gainers': supernova_gainers,
		'supernova_losers': supernova_losers,
		'pro_tickers': pro_tickers,
		'pro_gainers': pro_gainers,
		'pro_losers': pro_losers,
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
	"""
	given a set of ticker symbols as a single string, symbols separated by commas, find corresponding Ticker objects
	"""
	csv_elements = ticker_symbols_csv.split(',')

	# clean up - for each element, strip whitespace and convert to uppercase
	csv_elements = [el.strip().upper() for el in csv_elements]

	return Ticker.objects.filter(ticker_symbol__in=csv_elements)

def _get_service_objects_for_service_ids(service_ids_csv='1,4,7'):
	"""
	given a set of db ids of services, find corresponding Service objects
	# note: these ids were assigned by our db. they are *not* the service's product ids (eg Rule Breakers might have
		a product id of 1069, but in our db, its db id might be 3)
	"""	
	csv_elements = service_ids_csv.split(',')

	# clean up - for each element, strip whitespace and convert to an integer
	csv_elements = [int(el.strip()) for el in csv_elements]

	return Service.objects.filter(id__in=csv_elements)

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