from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
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
