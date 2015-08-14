import urllib
import json
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from risk_ratings.models import Ticker

TICKERS_SUMMARY_FILENAME = 'tickers_for_capiq.txt'

BASE_URL = "http://www.fool.com/a/PremiumScorecards/v1/scorecards/"
API_KEY = 'eb730eca-42d9-4840-8003-d29aa2e30580'

SCORECARDS = ['@StockAdvisorDavidInclusion', '@StockAdvisorTomInclusion', '@RuleBreakersInclusion',
    'Schwab-Deep-Value', 'Schwab-Hidden-Gems', 'Schwab-Special-Ops', 'Schwab-MDP-Charter',
    'IB-Everlasting', '@IncomeInvestorInclusion', '@InsideValueInclusion', '@HiddenGemsInclusion']

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        script_start_time = datetime.now()

        for scorecard in SCORECARDS:
            print 'processing %s' % scorecard

            url = BASE_URL + scorecard + "?apikey=%s" % API_KEY

            data = json.loads(urllib.urlopen(url).read())

            positions = data['OpenPositions'] + data['ClosedPositions']

            print '   positions: %d' % len(positions)

            for position in positions:
                if 'TickerSymbol' in position:
                    ticker_symbol = position['TickerSymbol']
                elif 'SecuritySymbol' in position:
                    ticker_symbol = position['SecuritySymbol']

                exchange_symbol = position['ExchangeSymbol']

                # throw out these cases:
                #   - we can't identify ticker
                #   - ticker is delisted
                #   - we can't identify exchange
                if not ticker_symbol or '.DL' in ticker_symbol:
                    continue
                if not exchange_symbol:
                    continue

                ticker_symbol = ticker_symbol.split(' ')[0].upper()
                company_name = position['CompanyName'][:150].upper()
                instrument_id = position['InstrumentId']

                try:
                    ticker = Ticker.objects.get(instrument_id=instrument_id,
                    exchange=exchange_symbol, symbol=ticker_symbol,
                    company_name=company_name)
                except:
                    ticker = Ticker.objects.create(instrument_id=instrument_id,
                    exchange=exchange_symbol, symbol=ticker_symbol,
                    company_name=company_name)

                    ticker.save()

        print 'tickers:', Ticker.objects.count()
    	print 'finished script'
        seconds_elapsed = (datetime.now() - script_start_time).total_seconds()
        print 'total seconds:', seconds_elapsed

        TICKERS_SUMMARY_FILENAME = 'tickers_for_capiq.txt'
        print 'writing tickers to file %s' % TICKERS_SUMMARY_FILENAME
        with open(TICKERS_SUMMARY_FILENAME, 'w') as file:
            tickers = Ticker.objects.all().order_by('symbol')

            # insert a trailing space, to deal with tickers like TRUE that would getevaluated as a boolean
            file.write('\n'.join([t.symbol.replace('-','.')+" " for t in tickers]))
        print 'wrote tickers'
