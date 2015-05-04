from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from forms import ArticlesFilterForm
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
		<p><a href='/sol/articles_vomit/'>Everything you ever wanted to know about articles</a></p>
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

	contains a form that lets you specify services

	if a service name is detected in the request's POST dictionary, then filters to tickers for that service
	"""

	services_to_filter_by = None 	# will hold the Service objects that satisfy our filter
	service_filter_description = None   # this will be a string description of the service filter. we'll display this value on the page.
	service_options = Service.objects.all()

	#---- start of handling a service filter submitted via POST request ---------

		# figure out what services were selected in the form. 
		# we've coded the html so that the input checkboxes are named 'filter_service_x', where
		# x is the id of a service, and the value is also the id of a service
		# in this step, we find out which of those 'filter_service_x' have been passed back in the POST
	service_filter_keys = [k for k in request.POST.keys() if k.startswith('filter_service_')]
	if len(service_filter_keys):

		services_to_filter_by = []
		for key in service_filter_keys:
			service_id = request.POST[key]  # we know the value will be a service id, b/c that's how we coded the html!
			service_match_for_this_id = Service.objects.get(id=service_id) 
			services_to_filter_by.append(service_match_for_this_id)

		# make the pretty description of the services we found. 
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)
	else:	
		# user didn't specify any services. that's fine. our services_to_filter_by, earlier set to None, is untouched.
		pass
	#---- end of handling a service filter submitted via POST request ---------


	# get the set of tickers, filtered by service, if those filters are defined
	if services_to_filter_by:
		scorecards_of_services = Scorecard.objects.filter(service__in=services_to_filter_by)
		service_takes_of_scorecards = ServiceTake.objects.filter(scorecard__in=scorecards_of_services)
		tickers = set()
		for st in service_takes_of_scorecards:
			tickers.add(st.ticker)
		tickers = list(tickers)
		tickers.sort(key=lambda x: x.daily_percent_change, reverse=True)
		top_10_gainers = tickers[:10]
		tickers.sort(key=lambda x: x.daily_percent_change)
		top_10_losers = tickers[:10]
		upcoming_earnings_announcements = Ticker.objects.all().order_by('earnings_announcement')[:10]
		# I need to figure out how to discard any results of "none"

	else:
		# get all tickers, and sort by biggest mover
		tickers = Ticker.objects.all().order_by('-daily_percent_change')
		top_10_gainers = tickers[:10]
		top_10_losers = Ticker.objects.all().order_by('daily_percent_change')[:10]
		upcoming_earnings_announcements = Ticker.objects.all().order_by('earnings_announcement')[:10]

	num_tickers = len(tickers)
	print num_tickers, '!!!!!!!!!!!!!!!!'

	"""

	####### pagination goes here when you figure that out ###########################

	# and now, let's see if there's anything interesting in the PUT dictionary
	# one use case of the PUT dictionary: from form actions, where data is passed 
	# along in the request, just not as a query string
	if request.POST:
		
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
			ticker_to_update = Ticker.objects.get(id=ticker_id)

			ticker_to_update.notes = request.POST[key_of_ticker_note_data] # retrieve from the POST dictionary the user input corresponding to this Ticker object
			ticker_to_update.save() # write this update to the db!
			
			# print to console a sanity check
			print 'updated Ticker %s (id: %s). notes value: %s' % (ticker_to_update.ticker_symbol, ticker_id, ticker_to_update.notes)

	###############################################################################
	"""

	dictionary_of_values = {
		# 'form': movers_filter_form,
		# 'tickers_subset': tickers_subset,
		'tickers': tickers,
		'num_tickers' : num_tickers,
		'service_filter_description': service_filter_description,
		'services_to_filter_by': services_to_filter_by,
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