'''
posts to slack a listing of the tickers we estimate will be reporting earnings in the near future (today or tomorrow)

'''
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from satellite.models import Ticker

from satellite.slack_utils import post_message_to_slack


class Command(BaseCommand):
	help = 'posts to slack the tickers that will be reporting earnings today or tomorrow'

	def handle(self, *args, **options):
		print 'starting script'

		today_date = datetime.today().date()
		tomorrow_date = (datetime.today() + timedelta(days=1)).date()
		
		tickers_reporting_today = Ticker.objects.filter(earnings_announcement=today_date)
		tickers_reporting_tomorrow = Ticker.objects.filter(earnings_announcement=tomorrow_date)

		message_snippets = []
		message_snippets.append("*Companies reporting earnings today:*")
		if not tickers_reporting_today:
			message_snippets.append("_none_")
		else:
			for t in tickers_reporting_today:
				message_snippets.append("   - %s (*%s*) : _%s_" % (t.company_name, t.ticker_symbol, t.services_for_ticker))


		message_snippets.append("*Companies reporting earnings tomorrow* (%s):" % tomorrow_date.strftime("%a, %b %d, %Y"))
		if not tickers_reporting_tomorrow:
			message_snippets.append("_none_")
		else:
			for t in tickers_reporting_tomorrow:
				message_snippets.append("   - %s (*%s*) : _%s_" % (t.company_name, t.ticker_symbol, t.services_for_ticker))


		message_to_post = "\n".join(message_snippets)
		post_message_to_slack(message_to_post)

		print message_to_post
    	print 'finished script'
