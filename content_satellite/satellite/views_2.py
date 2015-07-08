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

	dictionary_of_values = {
	'tickers': tickers,
	}

	return render(request, 'satellite/upcoming_earnings.html', dictionary_of_values)
