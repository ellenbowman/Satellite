import urllib
import json
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from risk_ratings.models import RiskRatingRecord, Ticker

URL = "https://apiary.fool.com/api/secure/content/query/?tag_slugs=risk-rating&service_ids=1069,1081&stop=500&format=json"
#URL = "https://apiary.fool.com/napi/secure/content/query/?tag_slugs=risk-rating&format=json&service_ids=1069,18"
#URL = 'http://apiary.fool.com/napi/secure/content/query/?stop=750&format=json&service_ids=1069,1081'
#URL = 'http://apiary.fool.com/napi/secure/content/query/?service_ids=1069,1081&start=860&format=json'
class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        url = URL

        response = urllib.urlopen(url).read()
        print response[:100]
        data_records = json.loads(response)
        results = data_records

        print len(results)

        for dr in results:
            no_risk_rating_tag = True
            for t in dr['tags']:
                if t['slug'] == 'risk-rating':
                    no_risk_rating_tag = False
                    break

            if no_risk_rating_tag:
                continue

            try:
                record = RiskRatingRecord.objects.get(legacy_uri = dr['legacy_uri'])
            except:
                record = RiskRatingRecord()
                record.legacy_uri = dr['legacy_uri']

            record.publish_date = datetime.strptime(dr['publish_at'].split('T')[0], "%Y-%m-%d")
            record.author = dr['byline']
            record.headline = dr['headline']

            #figure out the ticker

            ticker = dr['three_ticker_list_display']
            ticker = ticker.replace('</span>','')
            last_close_tag = ticker.rfind('>')
            ticker = ticker[last_close_tag+1:].strip()

            try:
                ticker = Ticker.objects.get(symbol=ticker)
            except:

                continue

            record.ticker = ticker
            record.save()

        if 'continuation_url' in data_records:
            print data_records['continuation_url']


    	print 'finished script'
        print 'records:', RiskRatingRecord.objects.count()
