from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from forms import FilterForm
from models import Article, BylineMetaData, Service, Ticker, Scorecard, ServiceTake, AnalystForTicker, CoverageType, COVERAGE_CHOICES

###############################################################################

def upcoming_earnings(request):
	context = {
		'page-title': 'Upcoming Earnings',
	}

	tickers = Ticker.objects.all()
	tickers = sorted(tickers, key=lambda x: x.daily_percent_change, reverse=True)
	
	yesterday = (datetime.now() - timedelta(days=1)).date()

	tickers_sorted_by_earnings_date = [t for t in tickers if t.earnings_announcement != None and t.earnings_announcement>yesterday]
	tickers_sorted_by_earnings_date = sorted(tickers_sorted_by_earnings_date, key=lambda x: x.earnings_announcement)[:100]

	for t in tickers_sorted_by_earnings_date:
		if t.services_for_ticker is not None:
			list_of_services = t.services_for_ticker.split(",")
			number_of_services = len(list_of_services)


	dictionary_of_values = {
	'tickers': tickers,
	'tickers_sorted_by_earnings_date': tickers_sorted_by_earnings_date,
	'list_of_services': list_of_services,
	'number_of_services': number_of_services,
	'form': FilterForm,
	}

	return render(request, 'satellite/upcoming_earnings.html', dictionary_of_values)

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


def get_author_bylines_index(request):

	dictionary_of_values = {
		'bylines_meta_data': BylineMetaData.objects.all().exclude(services='').order_by('byline')
	}

	return render(request, 'satellite/author_bylines_index.html', dictionary_of_values)

###########################################################################################################

def grand_vision_articles(request):


	tickers_to_filter_by = None
	services_to_filter_by = None
	ticker_filter_description = None
 	service_filter_description = None

	page_num = 1

	if request.POST:
		if 'page_number' in request.POST:
			page_num = int(request.POST['page_number'])

		article_filter_form = FilterForm(request.POST)
		
		if article_filter_form.is_valid():
			if 'tickers' in article_filter_form.cleaned_data:
				tickers_user_input = article_filter_form.cleaned_data['tickers'].strip()
				if tickers_user_input != '':
					tickers_to_filter_by = _get_ticker_objects_for_ticker_symbols(tickers_user_input)

			if 'services' in article_filter_form.cleaned_data:
				if len(article_filter_form.cleaned_data['services']) > 0:
					services_to_filter_by = article_filter_form.cleaned_data['services']

	elif request.GET:
		initial_form_values = {}

		if 'tickers' in request.GET:
			tickers_user_input = request.GET.get('tickers')
			tickers_to_filter_by = _get_ticker_objects_for_ticker_symbols(tickers_user_input)

			initial_form_values['tickers'] = tickers_user_input
		if 'service_ids' in request.GET:
			services_to_filter_by = _get_service_objects_for_service_ids(request.GET.get('service_ids'))
			initial_form_values['services'] = services_to_filter_by

		article_filter_form = FilterForm(initial=initial_form_values)

	else:
		article_filter_form = FilterForm()


	if tickers_to_filter_by:
		ticker_filter_description = ', '.join([t.strip() for t in tickers_user_input.split(",")])
	if services_to_filter_by:
		pretty_names_of_services_we_matched = [s.pretty_name for s in services_to_filter_by]
		pretty_names_of_services_we_matched.sort()
		service_filter_description = ', '.join(pretty_names_of_services_we_matched)


	if tickers_to_filter_by is not None and services_to_filter_by is not None:
		articles = Article.objects.filter(ticker__in=tickers_to_filter_by, service__in=services_to_filter_by).order_by('-date_pub')
	elif tickers_to_filter_by is not None:
		articles = Article.objects.filter(ticker__in=tickers_to_filter_by).order_by('-date_pub')
	elif services_to_filter_by is not None:
		articles = Article.objects.filter(service__in=services_to_filter_by).order_by('-date_pub')		
	else:
		articles = Article.objects.all().order_by('-date_pub')


	paginator = Paginator(articles, 100) 

	try:
		articles_subset = paginator.page(page_num)
	except PageNotAnInteger:
		# page is not an integer; let's show the first page of results
		articles_subset = paginator.page(1)
	except EmptyPage:
		# the user asked for a page way beyond what we have available;
		# let's show the last page of articles, which we can calculate
		# with paginator.num_pages
		articles_subset = paginator.page(paginator.num_pages)


	if len(articles):
		article_most_recent_date = articles[0].date_pub  
		article_oldest_date = articles[len(articles)-1].date_pub
	else:
		article_most_recent_date = "n/a"
		article_oldest_date = "n/a"

	authors = [art.author for art in articles]
	authors_set = set(authors)
	num_authors = len(authors_set)

	num_articles = len(articles)


	article_defns = []

	for article in articles_subset:

		byline_meta_data = ''

		byline_match = BylineMetaData.objects.filter(byline=article.author)
		if byline_match:
			byline_meta_data = byline_match[0].services

		article_defns.append({
			'article':article,
			'author_service_associations': byline_meta_data,
			})

	dictionary_of_values = {
		'form': article_filter_form,
		'articles': articles_subset,
		'article_defns': article_defns,
		'pub_date_newest': article_most_recent_date,
		'pub_date_oldest': article_oldest_date,
		'num_authors' : num_authors,
		'num_articles' : num_articles,
		'service_filter_description': service_filter_description,
		'ticker_filter_description': ticker_filter_description
	}

	return render(request, 'satellite/index_of_articles.html', dictionary_of_values)

###################################################################################

def ticker_lookup(request):
	"""
	returns json.  if the request contains a string of ticker symbols in its query string,
	then let the json be a dictionary with keys for each ticker symbol, value (True/False), for whether SOL knows about it.

	if no ticker symbols are detected, return a dictionary with a key of 'message'.
	"""

	# is there a 'tickers=x,y,z' in the query string? if so, let's process it
	if request.GET and 'tickers' in request.GET:

		ticker_symbols = request.GET['tickers']
		
		# proces the tickers; split into individual symbols, remove whitespace, and convert to uppercase
		ticker_symbols = ticker_symbols.split(',')
		ticker_symbols = [ts.strip().upper() for ts in ticker_symbols]

		response = {}
		# for each ticker symbol, we report whether SOL has a corresponding Ticker
		for ts in ticker_symbols:
			if Ticker.objects.filter(ticker_symbol=ts):
				response[ts] = True
			else:
				response[ts] = False

	else:
		response = {'message':'error: no tickers found in the query string'}

	# instead of rendering an html page, let's return this plain dictionary as a JsonResponse object.
	# https://docs.djangoproject.com/en/1.7/ref/request-response/#jsonresponse-objects
	# (the page won't have pretty markup)
	return JsonResponse(response)
