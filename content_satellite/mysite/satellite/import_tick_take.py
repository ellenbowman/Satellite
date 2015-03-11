import urllib
import json
from models import Scorecard
from models import Ticker

base_url = 'http://apiary.fool.com/PremiumScorecards/v1/scorecards/'

for scorecard in Scorecard.objects.all():
    print scorecard
    scorecard_name = scorecard.name

    url = base_url + scorecard_name

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
        """
        # create a ServiceTake
        st = ServiceTake()
        st.isCore = o['IsCore']
        st.ticker = t
        st.scorecard = scorecard
        st.save()
        """
