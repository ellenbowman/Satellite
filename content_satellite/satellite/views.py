from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from forms import FilterForm, TickerForm, CoverageTypeForm
from models import Article, BylineMetaData, Service, Ticker, Scorecard, ServiceTake, AnalystForTicker, CoverageType, COVERAGE_CHOICES

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

		ticker_note_name_prefix = 'ticker_notes_'

		keys_of_ticker_note_data = [key_in_post_dict for key_in_post_dict in request.POST.keys() if key_in_post_dict.startswith(ticker_note_name_prefix)]

		for key_of_ticker_note_data in keys_of_ticker_note_data:

			ticker_id = key_of_ticker_note_data[len(ticker_note_name_prefix):]
			print ticker_id
			ticker_to_update = Ticker.objects.get(ticker_symbol=ticker_id)

			ticker_to_update.notes = request.POST[key_of_ticker_note_data]
			ticker_to_update.save()

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


	if services_to_filter_by:
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

	if tickers_to_filter_by is not None and services_to_filter_by is not None:
		tiered_stocks = []
		for t in tickers_to_filter_by:
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker and t.tier is not 0:
					tiered_stocks.append(t)
					break

	elif services_to_filter_by is not None:
		tiered_stocks = []
		for t in Ticker.objects.all():
			if t.services_for_ticker is None:
				continue
			for service in services_to_filter_by:
				if service.pretty_name in t.services_for_ticker and t.tier is not 0:
					tiered_stocks.append(t)
				break

	elif tickers_to_filter_by is not None:
		tiered_stocks = tickers_to_filter_by

	else:
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
	yesterday = (datetime.now() - timedelta(days=1)).date()
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


	yesterday = (datetime.now() - timedelta(days=1)).date()

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

######################################################################################

def ticker_overview(request):

	dictionary_of_values = {
		'title_value': 'All Tickers',
		'services': Service.objects.all(),
		'tickers': Ticker.objects.all(),
	}
	return render(request, 'satellite/tickers_index.html', dictionary_of_values)

###############################################################################

def ticker_detail(request, ticker_symbol):

	try:
		ticker = Ticker.objects.get(ticker_symbol=ticker_symbol)
	except:
		# if the ticker isn't found, redirect to the listing of all tickers
		return redirect('ticker_overview')

	if request.POST:
		form = TickerForm(request.POST, instance=ticker)

		if form.is_valid():
			model_instance = form.save(commit=True)

	form = TickerForm(instance=ticker)

	context = {
		'title_value': '%s (%s)' % (ticker.company_name, ticker.ticker_symbol),
		'form': form,
		'ticker':ticker
	}

	return render(request, 'satellite/ticker_detail.html', context)

###############################################################################

def coverage_detail(request, ticker_symbol):

	try:
		ticker = Ticker.objects.get(ticker_symbol=ticker_symbol)
	except:
		# if the ticker isn't found, redirect to the listing of all tickers
		return redirect('coverage_index')

	services_to_filter_by = None
	service_filter_description = None
	tickers_to_filter_by = None
	single_authors = get_authors_from_article_set()
	form = TickerForm(instance=ticker)

	if request.POST:

		form = TickerForm(request.POST, instance=ticker)
		if form.is_valid():
			model_instance = form.save(commit=True)

		if 'coverage' in request.POST:

			# delete records that are already there
			coverage_type_objects = CoverageType.objects.filter(ticker=ticker)
			print 'deleting existing CoverageType records for %s (%d)' % (ticker.ticker_symbol, len(coverage_type_objects))
			coverage_type_objects.delete()

			# replace them with the records passed along in POST
			# we expect the keys per selection to have this format: "cid_x__sid_y", where x is a content choice integer value, y is a service id
			selected_keys = [k for k in request.POST if k.startswith('author_')]
			for k in selected_keys:

				k = k.replace('author_','')
				print k, '---------------'
				choice_id, service_id = k.replace("cid_","").replace("sid_","").split('__')

				ct = CoverageType()
				ct.coverage_type = int(choice_id)
				ct.ticker = ticker
				ct.service = Service.objects.get(id=service_id)

				author_key = 'author_'+k

				print author_key

				if author_key in request.POST:
					ct.author = request.POST[author_key]

				ct.save()
				print 'added CoverageType record: %s %s %d %s' % (ct.service.pretty_name, ct.ticker.ticker_symbol, ct.coverage_type, ct.author)
		else:
			pass
		
	else:
		pass

	services = Service.objects.all()
	
	today = datetime.now()
	date_today = today.date()
	ninety_days_ago = (date_today - timedelta(days=90))

	articles = [a for a in Article.objects.filter(ticker=ticker).exclude(tags=None).exclude(tags='') if a.date_pub is not None and a.date_pub.date() >= ninety_days_ago]

	relevant_articles = set()
	ten_percent_promises = set()
	everlasting = set()
	analysis = set()
	featured = set()
	earnings = set()
	mission_log = set()
	buy_recommendations = set()
	five_and_three = set()
	best_buys_now = set()
	two_minute_drills = set()
	commentary = set()
	news = set()

	for a in articles:
		if '10 promise' in a.tags:
			ten_percent_promises.add(a)
		if 'everlasting' in a.tags:
			everlasting.add(a)
		if 'analysis' in a.tags:
			analysis.add(a)
		if 'featured' in a.tags:
			featured.add(a)
		if 'earnings' in a.tags:
			earnings.add(a)
		if 'mission_log' in a.tags:
			mission_log.add(a)
		if 'buy recommendation' in a.tags:
			buy_recommendations.add(a)
		if '5 and 3' in a.tags:
			five_and_three.add(a)
		if 'best buys now' in a.tags:
			best_buys_now.add(a)
		if '2 minute drill' in a.tags:
			two_minute_drills.add(a)
		if 'commentary' in a.tags:
			commentary.add(a)
		if 'news' in a.tags:
			news.add(a)

	print request.POST

	dictionary_of_values = {
		'ticker': ticker,
		'form': form,
		'coverage_type_choices': COVERAGE_CHOICES,
		'services': services,
		'single_authors': single_authors,
		'title_value': '%s (%s)' % (ticker.company_name, ticker.ticker_symbol),
		'relevant_articles': relevant_articles,
		'ten_percent_promises': ten_percent_promises,
		'everlasting': everlasting,
		'featured': featured,
		'earnings': earnings,
		'mission_log': mission_log,
		'buy_recommendations': buy_recommendations,
		'five_and_three': five_and_three,
		'best_buys_now': best_buys_now,
		'two_minute_drills': two_minute_drills,
		'commentary': commentary,
		'news': news,
	}

	return render(request, 'satellite/coverage_detail.html', dictionary_of_values)

###############################################################################

def get_service_ids(coverage_type_id, ticker_symbol):
	all_coverage_choices = CoverageType.objects.all()
	for a in all_coverage_choices:
		if coverage_type_id != a.coverage_type:
			pass
		else:
			print coverage_type_id

	return coverage_type_id

#################################################################################

def get_authors_from_article_set():
	all_authors_ever = [a.byline for a in BylineMetaData.objects.all()]
	sep = ' and'
	authors_no_and = [a.split(sep, 1)[0] for a in all_authors_ever]
	sep = ','
	single_authors = [a.split(sep, 1)[0] for a in authors_no_and]
	single_authors = set(single_authors)
	single_authors = list(single_authors)
	single_authors.sort()
	return single_authors

###############################################################################

def coverage_index(request):

	coverage_types = CoverageType.objects.all()

	dictionary_of_values = {
	'title_value': 'All Tickers',
	'services': Service.objects.all(),
	'tickers': Ticker.objects.all(),
	'coverage_types': CoverageType.objects.all(),
		}

	return render(request, 'satellite/coverage_index.html', dictionary_of_values)


###############################################################################
