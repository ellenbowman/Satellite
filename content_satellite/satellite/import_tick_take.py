import urllib
import json
from models import Scorecard
from models import Ticker
from models import ServiceTake
import datetime

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
        
