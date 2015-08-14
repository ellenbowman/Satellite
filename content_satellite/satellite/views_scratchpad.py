import urllib
import json
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from forms import FilterForm, TickerForm
from django.db.models import Q
from models import Article, BylineMetaData, Service, Ticker, Scorecard, ServiceTake, \
	AnalystForTicker, CoverageType, COVERAGE_CHOICES, DataHarvestEventLog, DATA_HARVEST_TYPE_CHOICES


def articles_on_demand(request, ticker_symbol):
    context = {
        'ticker_symbol': ticker_symbol
    }

    ticker_symbol = ticker_symbol.upper()
    try:
        ticker = Ticker.objects.get(ticker_symbol = ticker_symbol)
    except:
        context['error_message'] = "Sorry, SOL doesn't recognize ticker " % ticker_symbol

    if ticker:
        service_ids = '1081,1069,1502,1451,1371,1321,1255,1228,1128,1066,1062,1048,1008'

        url = 'http://apiary.fool.com/napi/secure/content/query/?stop=100&format=json&service_ids=%s&instrument_ids=%d' % (service_ids, ticker.instrument_id )
        resp = urllib.urlopen(url)

        article_data = json.loads(resp.read())['results']

        articles_keyed_by_tag = {}
        articles_keyed_by_tag['intel'] = []
        articles_keyed_by_tag['analysis'] = []
        articles_keyed_by_tag['mission'] = []
        articles_keyed_by_tag['earnings'] = []
        articles_keyed_by_tag['risk'] = []
        articles_keyed_by_tag['recommendation'] = []

        for a in article_data:
            tag_slugs = [tag['slug'] for tag in a['tags']]
            tag_slugs_as_csv = ','.join(tag_slugs)

            for t in articles_keyed_by_tag.keys():
                if t in tag_slugs_as_csv:
                    articles_keyed_by_tag[t].append(a)

        # remove keys that have no articles
        keys_with_zero_hits = [k for k in articles_keyed_by_tag.keys() if len(articles_keyed_by_tag[k])==0]
        for k in keys_with_zero_hits:
            del articles_keyed_by_tag[k]

        context['ticker'] = ticker
        context['articles_by_tag'] = articles_keyed_by_tag

    return render(request, 'satellite/scratchpad_ticker_articles.html', context)
