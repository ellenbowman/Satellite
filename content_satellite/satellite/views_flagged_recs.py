import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from models import ServiceTake, Ticker


def _get_profiles_of_flagged_recs():
	"""
	returns a list of dictionary elements, one element per ticker/scorecard combo, where the
	tickers are limited to the set flagged as at least one of these: a core buy, a buy first, or a new rec

	the list will be ordered by ticker (if HG and SA scorecards both flagged ticker AAPL, then elements for AAPL/HG and AAPL/SA would be grouped together)

	an example of what a dictionary element might look like:
		{
			'ticker_symbol': 'AAPL',
			'company': "Apple",
			'service_pretty_name': "Stock Advisor",
			'scorecard_pretty_name': "Stock Advisor - Tom",
			'action': "buy",
			'open_dates': "2014-03-02,<br/>2012-03-01",
			'is_core':True,
			'is_first':False,
			'is_new': False,
			'daily_percent_change': 0.31
		}


	"""
	flagged_rec_defns = []


	# let's find all the ServiceTake objects that satisfies at least one of these: is a "core buy", "buy first", or new rec. 
	# http://stackoverflow.com/questions/739776/django-filters-or
	flagged_service_takes = ServiceTake.objects.filter(Q(is_core=True) | Q(is_first=True) | Q(is_newest=True))


	# we want one profile per ticker/scorecard combo. 
	# but... it's possible that we'll have cases where a scorecard has flagged a ticker, and the scorecard has a history of adding a position in that ticker
	# (AAPL might be a current BBN for the SA David scorecard, and that scorecard might have opened positions on AAPL on 3 occasions)
	# in that case, let's summarize the open dates into a single string.
	# one way to implement that: we'll organize our results by ticker, and from there (per ticker) inspect 
	# the cases where a scorecard appears multiple times. along the way, we compile flagged_rec_defns

	# compile a set of the ticker symbols that are flagged
	ticker_symbols_in_flagged_service_takes = [st.ticker.ticker_symbol for st in flagged_service_takes]
	ticker_symbols_in_flagged_service_takes = set(ticker_symbols_in_flagged_service_takes)  # convert to a set, to toss out duplicates
	ticker_symbols_in_flagged_service_takes = list(ticker_symbols_in_flagged_service_takes)  # convert back to a list, so that we can impose an order
	ticker_symbols_in_flagged_service_takes.sort()   # will sort by alphabetical order


	# now let's go through the flagged service takes, inspecting cases per ticker. 
	# ie, if we have ['AAPL', 'BOFI','DIS'] in ticker_symbols_in_flagged_service_takes, then we'll first 
	# process all of the flagged service takes that are for the AAPL ticker, then we'll process those for the BOFI ticker, etc.
	
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


def get_flagged_recs_index(request):

	dictionary_of_values = {
		'flagged_rec_defns': _get_profiles_of_flagged_recs()
	}

	return render(request, 'satellite/flagged_recs_index.html', dictionary_of_values)


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
