import urllib
import json
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from risk_ratings.models import Ticker, TickerProfile

BASE_URL = "http://www.fool.com/a/quotes/v3/Instrument/GetCompetitors/"
API_KEY = 'eb730eca-42d9-4840-8003-d29aa2e30580'

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        script_start_time = datetime.now()

        for ticker_profile in TickerProfile.objects.all():

            url = BASE_URL + "?instrumentId=%d&apikey=%s" % (ticker_profile.ticker.instrument_id, API_KEY)
            data = json.loads(urllib.urlopen(url).read())

            competitors = ["%s (%s)" % (d['Name'], d['Symbol']) for d in data]

            ticker_profile.competitors = '; '.join(competitors)
            ticker_profile.save()

    	print 'finished script'
        print 'tickerProfiles:', TickerProfile.objects.count()

        seconds_elapsed = (datetime.now() - script_start_time).total_seconds()
        print 'total seconds:', seconds_elapsed
