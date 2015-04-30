'''
update the 'daily_percent_change' field on all Ticker objects
'''
import urllib2
import datetime
import json

from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker


def get_number_fool_one_followers(ticker_symbol):
	url='http://apiary.fool.com/leads/.json?serviceIds=1255&tickers=%s' % (ticker_symbol)
	lookie='Lookie=C6203A9167ABA57562DD83D6AEA13BCC1EDC892BE430D6915FA389C5437EDE6F4E8F70E752E1838A1C6343E400F5D8C230FB1395D04410E2049CA550A09989D258D66CC6C03D2201454FC58D4909FC982C45F62419E9EAFD323772179CB7C85F59970D042D2EB71BFD9F168B626BAA4A732E3E53A322D3CC4783BA8B56C6663A39BC100F'

	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', lookie.strip()))

	response = opener.open(url, timeout=10).read()
	json_response = json.loads(response)
	num_followers = json_response['SubscribersFollowingTicker']
	return num_followers


class Command(BaseCommand):
    def handle(self, *args, **options):
		print 'starting script'

		script_start_time = datetime.datetime.now()
		tickers = Ticker.objects.all().order_by('ticker_symbol')
		for ticker in tickers:
			ticker_symbol = ticker.ticker_symbol

			try:
				num_followers = get_number_fool_one_followers(ticker_symbol)
				print ticker, num_followers
				ticker.num_followers = num_followers
				ticker.save()
			except Exception as e:
				print "couldn't set number of followers", str(e)

		script_end_time = datetime.datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds
		print 'finished script'