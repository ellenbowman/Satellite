'''
posts to slack an overview of the daily market performance of each service's recs
(per service: top 3 gainers; worst 3 losers; what % of the recs had positive movement)
'''
from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from satellite.models import Service, Ticker

from satellite.slack_utils import post_message_to_slack

"""
sample of what the output to slack:

Ticker performance snapshot for Thu, May 28, 2015  04:32 
(per service: top 3 gainers; top 3 losers; % of recs with positive movement)
[...]
 - Hidden Gems
      ENOC (3.55%),  ALV (2.92%),  SLCA (2.85%)
      SAVE (-6.68%),  RAVN (-4.43%),  LL (-4.24%)
      recs with gains: 41.30% (38 of 92)
 - Income Investor
      SSL (2.02%),  OKS (1.8%),  OAK (1.54%)
      SBS (-3.79%),  NSH (-2.57%),  MHLD (-2.17%)
      recs with gains: 47.89% (34 of 71)
[...] 

"""
class Command(BaseCommand):
	help = "posts to slack an overview of the daily market performance of each service's recs"

	def handle(self, *args, **options):
		print 'starting script'

		# create a dictionary, keys = service pretty name, values = a list of tickers in that service
		tickers_by_service_pretty_name = {}

		# prime the dictionary: insert keys for the service pretty names, set the values to an empty list
		for s in Service.objects.all():
			tickers_by_service_pretty_name[s.pretty_name] = []

		# populate the values
		for ticker in Ticker.objects.all():
			if not ticker.services_for_ticker:
				continue
			
			# convert the string of services into a list, one element per service name
			services_associated_with_ticker = ticker.services_for_ticker.split(",")

			# strip whitespace from each element in the list
			services_associated_with_ticker = [s.strip() for s in services_associated_with_ticker] 

			for service_associated_with_ticker in services_associated_with_ticker:
				tickers_by_service_pretty_name[service_associated_with_ticker].append(ticker)


		# by this point, we've iterated over all tickers and via our dictionary know
		# all that are associated to any service
		# we'll now compile text summaries, one per service

		text_summaries = []

		service_pretty_names = tickers_by_service_pretty_name.keys()
		service_pretty_names.sort()
		for service_pretty_name in service_pretty_names:

			print 'processing tickers for service ', service_pretty_name

			tickers_for_this_service = tickers_by_service_pretty_name[service_pretty_name]
			ticker_count_for_this_service = len(tickers_for_this_service)

			print 'how many tickers?', ticker_count_for_this_service

			if ticker_count_for_this_service == 0:
				text_summaries.append("  - %s: no tickers" % service_pretty_name)
				continue

			tickers_for_this_service = sorted(tickers_for_this_service, key=lambda x: x.daily_percent_change, reverse=True)

			top_gainers = tickers_for_this_service[:3]
			top_losers = tickers_for_this_service[-3:]
			top_losers.reverse()  # so that this smaller list is ordered from worst performance to less bad performance


			tickers_with_positive_movement = [t for t in tickers_for_this_service if t.daily_percent_change > 0.0]
			count_tickers_with_positive_movement = len(tickers_with_positive_movement)


			# we've identified the data points (top gainers, top losers, count of the tickers with positive movement);
			# now let's create the text description. 
			# https://docs.python.org/2/library/string.html#format-specification-mini-language
			# https://docs.python.org/2/library/string.html
			desc_of_top_gainers = [' %s (%g%%)' % (t.ticker_symbol, t.daily_percent_change) for t in top_gainers]
			desc_of_top_gainers = ', '.join(desc_of_top_gainers)

			desc_of_top_losers = [' %s (%g%%)' % (t.ticker_symbol, t.daily_percent_change) for t in top_losers]
			desc_of_top_losers = ', '.join(desc_of_top_losers)

			percentage_positive_movement = '{:.2%}'.format(1.0*count_tickers_with_positive_movement/ticker_count_for_this_service)
			desc_of_positive_movement = "recs with gains: %s (%d of %d)" % (percentage_positive_movement, count_tickers_with_positive_movement, ticker_count_for_this_service)

			summary_for_this_service  = "  - %s" % (service_pretty_name)
			summary_for_this_service += "\n      %s" % desc_of_top_gainers
			summary_for_this_service += "\n      %s" % desc_of_top_losers
			summary_for_this_service += "\n       %s" % desc_of_positive_movement

			text_summaries.append(summary_for_this_service)
			print summary_for_this_service


		text_summaries.insert(0, "*Ticker performance snapshot for %s *" % datetime.now().strftime('%a, %b %d, %Y  %H:%M'))  # eg: Tue, May 12, 2015 11:15
		text_summaries.insert(1, "(per service: top 3 gainers; top 3 losers; % of recs with positive movement)")
		
		message_to_post = "\n".join(text_summaries)

		post_message_to_slack(message_to_post)

    	print 'finished script'
