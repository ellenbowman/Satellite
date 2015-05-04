from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from forms import FilterForm
from models import Article, Service, Ticker, Scorecard, ServiceTake

# Create your views here.

###############################################################################

### will make way for info_by_scorecard or something quite like it

def index(request):
	context = {
		'page-title': 'Welcome to the Satellite'
	}

	return HttpResponse("""
		<div align='center'; style='font-family:Verdana, Arial, Helvetica, sans-serif'>
		<h3>A bunch of our ship fell off, and nobody likes me.</h3>
		<p><a href='/admin/satellite/ticker/'>Ticker view: admin</a></p>
		<p><a href='/sol/articles_index/'>Everything you ever wanted to know about articles</a></p>
		<p><a href='/sol/movers_by_service/'>Today's biggest movers by service</a></p>
		</div>
		""", context)

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

# ServiceTakes have both a ticker and a scorecard, and a scorecard has a service.
# So show me ServiceTakes by scorecard?

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

def movers_by_service(request):
# copied from grand_vision_articles
	"""
	shows all tickers and some meta data
	(daily percent change, company name, exchange, ticker symbol)

	contains a form that lets you specify services and tickers

	if a service or ticker's name is detected in the request's POST dictionary, then filters to tickers for that service or ticker
	"""

	services_to_filter_by = None 	# will hold the Service objects that satisfy our filter
	service_filter_description = None   # this will be a string description of the service filter. we'll display this value on the page.
	tickers_to_filter_by = None
	ticker_filter_description = None
	service_options = Service.objects.all()

	page_num = 1


	# filter by ticker/service if we detect that preference in the query string (in the request.GET)
	# or via a form post (in the request.POST)
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
				# the form makes available "cleaned data" that's pretty convenient - 
				# in this case, it returns a list of Service objects that correspond
				# to what the user selected.
				services_to_filter_by = movers_filter_form.cleaned_data['services']

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


	# get the set of articles, filtered by ticker/service, if those filters are defined
	if tickers_to_filter_by is not None and services_to_filter_by is not None:
		tickers = Ticker.objects.filter(ticker_symbol__in=tickers_to_filter_by).order_by('-daily_percent_change')
	elif tickers_to_filter_by is not None:
		tickers = Ticker.objects.filter(ticker_symbol__in=tickers_to_filter_by).order_by('-daily_percent_change')
	elif services_to_filter_by is not None:
		tickers = Ticker.objects.filter(servicetake__in=services_to_filter_by).order_by('-daily_percent_change')		
	else:
		# get all articles, and sort by descending date
		tickers = Ticker.objects.all().order_by('-daily_percent_change')

	# introduce django's built-in pagination!! 
	# https://docs.djangoproject.com/en/1.7/topics/pagination/
	paginator = Paginator(tickers, 25) 


	try:
		tickers_subset = paginator.page(page_num)
	except PageNotAnInteger:
		# page is not an integer; let's show the first page of results
		tickers_subset = paginator.page(1)
	except EmptyPage:
		# the user asked for a page way beyond what we have available;
		# let's show the last page of articles, which we can calculate
		# with paginator.num_pages
		tickers_subset = paginator.page(paginator.num_pages)

	num_tickers = len(tickers)
	top_10_gainers = tickers[:10]
	top_10_losers = tickers[:10]
	upcoming_earnings_announcements = "upcoming earnings announcements"


	dictionary_of_values = {
		'form': movers_filter_form,
		'tickers': tickers,
		'num_tickers' : num_tickers,
		'service_filter_description': service_filter_description,
		'services_to_filter_by': services_to_filter_by,
		'tickers_to_filter_by': tickers_to_filter_by,
		'service_options': service_options,
		'top_10_gainers': top_10_gainers,
		'top_10_losers': top_10_losers,
		'upcoming_earnings_announcements': upcoming_earnings_announcements,
		# 'ticker_filter_description': ticker_filter_description
	}

	return render(request, 'satellite/movers_by_service.html', dictionary_of_values)


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