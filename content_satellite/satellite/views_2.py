import csv
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from forms import FilterForm
from django.db.models import Q
from models import Article, BylineMetaData, Service, Ticker, Scorecard, ServiceTake, \
	AnalystForTicker, CoverageType, COVERAGE_CHOICES, DataHarvestEventLog, DATA_HARVEST_TYPE_CHOICES

###############################################################################

def upcoming_earnings(request):
	context = {
		'page-title': 'Upcoming Earnings',
	}

	tickers = Ticker.objects.all()
	tickers = sorted(tickers, key=lambda x: x.daily_percent_change, reverse=True)
	
	yesterday = (datetime.now() - timedelta(days=1)).date()

	tickers_sorted_by_earnings_date = [t for t in tickers if t.services_for_ticker != None and t.earnings_announcement != None and t.earnings_announcement>yesterday]
	tickers_sorted_by_earnings_date = sorted(tickers_sorted_by_earnings_date, key=lambda x: x.earnings_announcement)[:100]

	for t in tickers_sorted_by_earnings_date:
		list_of_services = t.services_for_ticker.split(",")
		number_of_services = len(list_of_services)
		print number_of_services

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

	csv_elements = [int(el.strip()) for el in csv_elements]

	return Service.objects.filter(id__in=csv_elements)


def get_author_bylines_index(request):

	dictionary_of_values = {
		'bylines_meta_data': BylineMetaData.objects.all().exclude(services='').order_by('byline')
	}

	return render(request, 'satellite/author_bylines_index.html', dictionary_of_values)

###########################################################################################################

def articles_index(request):

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

	return render(request, 'satellite/articles_index.html', dictionary_of_values)

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

######################################################################################################

def data_freshness_index(request):
	
	recent_events_overall = DataHarvestEventLog.objects.all().order_by('-date_started')[:100]

	most_recent_event_per_type = []
	
	for ht in DATA_HARVEST_TYPE_CHOICES:
		ht_id = ht[0]
		ht_pretty_name = ht[1]

		events_for_this_type = DataHarvestEventLog.objects.filter(data_type=ht_id).order_by('-date_started')
		date_of_most_recent_event_of_this_type = None
		if events_for_this_type:
			date_of_most_recent_event_of_this_type = events_for_this_type[0].date_started

		most_recent_event_per_type.append({
			'pretty_name':ht_pretty_name, 
			'type':ht_id, 
			'date':date_of_most_recent_event_of_this_type
			})

	dictionary_of_values = {
		'recent_events':recent_events_overall,
		'most_recent_event_per_type':most_recent_event_per_type
	}

	return render(request, 'satellite/data_freshness_index.html', dictionary_of_values)

################################################################################################

def _get_profiles_of_flagged_recs():
	
	"""
	returns a list of dictionary elements, one element per ticker/scorecard combo, where the
	tickers are limited to the set flagged as at least one of these: a core buy, a buy first, or a new rec
	the list will be ordered by ticker (if HG and SA scorecards both flagged ticker AAPL, then elements for AAPL/HG and AAPL/SA would be grouped together)
	"""
	flagged_rec_defns = []

	# let's find all the ServiceTake objects that satisfies at least one of these: is a "core buy", "buy first", or new rec. 
	flagged_service_takes = ServiceTake.objects.filter(Q(is_core=True) | Q(is_first=True) | Q(is_newest=True))


	# we want one profile per ticker/scorecard combo. we'll organize our results by ticker, and from there (per ticker) inspect 
	# the cases where a scorecard appears multiple times. along the way, we compile flagged_rec_defns

	# compile a set of the ticker symbols that are flagged
	ticker_symbols_in_flagged_service_takes = [st.ticker.ticker_symbol for st in flagged_service_takes]
	ticker_symbols_in_flagged_service_takes = set(ticker_symbols_in_flagged_service_takes)
	ticker_symbols_in_flagged_service_takes = list(ticker_symbols_in_flagged_service_takes)
	ticker_symbols_in_flagged_service_takes.sort()

	# now let's go through the flagged service takes, inspecting cases per ticker. 
	
	for ticker_symbol in ticker_symbols_in_flagged_service_takes:
		flagged_service_takes_on_this_ticker_symbol = [st for st in flagged_service_takes if st.ticker.ticker_symbol==ticker_symbol]

		# process this subset of service takes by scorecard
		scorecards_in_this_subset_of_ticker_specific_service_takes = [st.scorecard.pretty_name for st in flagged_service_takes_on_this_ticker_symbol]
		scorecards_in_this_subset_of_ticker_specific_service_takes = set(scorecards_in_this_subset_of_ticker_specific_service_takes)

		for scorecard_pretty_name in scorecards_in_this_subset_of_ticker_specific_service_takes:
			service_takes_to_process = [st for st in flagged_service_takes_on_this_ticker_symbol if st.scorecard.pretty_name==scorecard_pretty_name]
			open_dates = [st.open_date.strftime('%Y-%m-%d') for st in service_takes_to_process if st.open_date is not None]
			open_dates = set(open_dates)
			open_dates = list(open_dates)
			open_dates.sort(reverse=True)
			open_dates_as_string = '<br/>'.join(open_dates)

			sample_service_take_for_this_scorecard = service_takes_to_process[0]

			flagged_rec_defns.append({
				'ticker_symbol': ticker_symbol,
				'company': sample_service_take_for_this_scorecard.ticker.company_name,
				'service_pretty_name': sample_service_take_for_this_scorecard.scorecard.service.pretty_name,
				'scorecard_pretty_name': sample_service_take_for_this_scorecard.scorecard.pretty_name,
				'action':sample_service_take_for_this_scorecard.action,
				'open_dates': open_dates_as_string,
				'is_core':sample_service_take_for_this_scorecard.is_core,
				'is_first':sample_service_take_for_this_scorecard.is_first,
				'is_new': sample_service_take_for_this_scorecard.is_newest,
				'daily_percent_change': sample_service_take_for_this_scorecard.ticker.daily_percent_change
				})

	return flagged_rec_defns

####################################################################################################

def get_flagged_recs_index(request):

	dictionary_of_values = {
		'flagged_rec_defns': _get_profiles_of_flagged_recs()
	}

	return render(request, 'satellite/flagged_recs_index.html', dictionary_of_values)

####################################################################################################

def get_flagged_recs_as_csv(request):
	"""
	return a csv version of the flagged recs
	"""
	flagged_rec_defns = _get_profiles_of_flagged_recs()

	response = HttpResponse(content_type='text/csv')

	response['Content-Disposition'] = 'attachment; filename="satellite_flagged_recs.csv"'

	# here we write out, line-by-line, the file's contents
	# because it's a csv, we'll be careful that no cell includes a comma
	writer = csv.writer(response)
	writer.writerow(['ticker','company','service','scorecard','action','open dates','new','buy first', 'core'])
	for frd in flagged_rec_defns:
		row_to_write = []
		row_to_write = [frd['ticker_symbol'], frd['company'].replace(",",""), frd['service_pretty_name'].replace(",",""), frd['scorecard_pretty_name'].replace(",",""), frd['action']]
		row_to_write.append(frd['open_dates'].replace('<br/>', ', '))
		row_to_write.append('Y' if frd['is_new'] else '')
		row_to_write.append('Y' if frd['is_first'] else '')
		row_to_write.append('Y' if frd['is_core'] else '')

		writer.writerow(row_to_write)

	return response

