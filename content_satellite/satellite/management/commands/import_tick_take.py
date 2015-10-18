'''
creates Ticker objects if necessary
updates services/scorecards for ticker
updates the ServiceTake objects, adding BBN, new, core status
'''

import urllib
import json
import datetime
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Ticker, Scorecard, ServiceTake
from django.conf import settings
from satellite.models import Article, Service, Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_SCORECARD_RECS

base_url = 'http://apiary.fool.com/PremiumScorecards/v1/scorecards/'

class Command(BaseCommand):
    help = "Imports core, first, BBN, new rec information for tickers."

    def handle(self, *args, **options):
        print "Let's do this"

        event_log = DataHarvestEventLog()
        event_log.data_type = DATA_HARVEST_TYPE_SCORECARD_RECS
        event_log.notes = 'running'
        event_log.save()

        script_start_time = datetime.datetime.now()
        notes = ''

        # delete all previous ServiceTakes
        ServiceTake.objects.all().delete()

        for scorecard in Scorecard.objects.all():
            print scorecard
            scorecard_name = scorecard.name
            url = base_url + scorecard_name
            print url
            response = urllib.urlopen(url).read()
            json_resp = json.loads(response)
            op = json_resp['OpenPositions']
            for o in op:
                ticker_symbol = o['UnderlyingTickerSymbol']
                if ticker_symbol=='':
                    ticker_symbol=o['TickerSymbol']

                print ticker_symbol
                # create a Ticker for this symbol if it doesn't exist
                matches = Ticker.objects.filter(ticker_symbol=ticker_symbol)        
                if len(matches)==0:
                    t = Ticker()
                    t.ticker_symbol = ticker_symbol
                    t.instrument_id = o['InstrumentId']
                    t.exchange_symbol = o['ExchangeSymbol']
                    t.percent_change_historical = 0.0
                    t.company_name = o['CompanyName']
                    t.save()
                else:
                    t = matches[0]

        
               # create a ServiceTake
                st = ServiceTake()
                st.is_core = o['IsCore']
                st.is_first = o['IsFirst']
                st.is_newest = o['IsNewest']
                st.action = o['Action']
                st.is_present = True
                st.ticker = t
                st.scorecard = scorecard
                temp = o['OpenDate']
                temp = temp.split('T')[0]
                st.open_date = datetime.datetime.strptime(temp, '%Y-%m-%d')

                st.save()

                #create scorecards_for_ticker and services_for_ticker
                service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=t)
                scorecards_for_ticker = list()
                for st in service_takes_on_this_ticker:
                    scorecards_for_ticker.append(st.scorecard.pretty_name)

                scorecards_for_ticker = set(scorecards_for_ticker)
                t.scorecards_for_ticker = ", ".join(scorecards_for_ticker)

                services_for_ticker = list()
                for st in service_takes_on_this_ticker:
                    services_for_ticker.append(st.scorecard.service.pretty_name)

                services_for_ticker = set(services_for_ticker)
                t.services_for_ticker = ", ".join(services_for_ticker)

                t.save()


            notes = 'updated Ticker objects'

        script_end_time = datetime.datetime.now()
        total_seconds = (script_end_time - script_start_time).total_seconds()

        print 'time elapsed: %d seconds' %  total_seconds
        event_log.notes = notes         
        event_log.save()

        print 'finished script'