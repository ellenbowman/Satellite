'''
ask the API for the most recent 100 articles across the premium services;
for each of those, add an Article object, one for each of the tickers in the article 
'''
import urllib
import json
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from satellite.models import Article, Service, Ticker, DataHarvestEventLog, DATA_HARVEST_TYPE_ARTICLES

num_articles_to_retrieve = 100
stop_value = num_articles_to_retrieve - 1  # the API treats the stop arg as zero-based and inclusive; eg to get 5 results, tell it to go up to (and include) index 4
service_ids = '1081,1069,1502,1451,1371,1321,1255,1228,1128,1066,1062,1048,1008'
url = 'http://apiary.fool.com/napi/secure/content/query/?stop=%d&format=json&service_ids=%s' % (stop_value, service_ids)

def get_articles():

	response = urllib.urlopen(url).read()
	json_data = json.loads(response)
	articles = json_data['results']

	print 'num articles returned from API:', len(articles)

	# for all of those articles, keep only the ones that have a 'tickers' value
	articles = [article for article in articles if article['tickers']]

	print 'num articles with tickers:', len(articles)

	count_of_articles_added = 0

	for article_json in articles:
		for ticker_defn in article_json['tickers']:
			instrument_id = ticker_defn['instrument_id']

			# does SOl have a ticker that corresponds to this instrument id?
			# if so, then we'll proceed with giving SOL a copy of this article
			# else, we'll skip this article
			ticker_matches = Ticker.objects.filter(instrument_id=instrument_id)
			if not ticker_matches:
				continue  # don't process the rest of the lines in this for loop

			ticker_match = ticker_matches[0]
		
			# examples of values we expect in ['service']['slug']: 'hidden_gems','stock_advisor','supernova'
			# we need to have corresponding Service records
			service_slug = article_json['service']['slug']
			# find those corresponding Service records. in practice, we should get at most 1 match
			service_matches = Service.objects.filter(name=service_slug)
			if len(service_matches)==0:
				# if we don't find a match, then assume we don't care to process the article
				print 'no match for service', service_slug
				continue

			# assign the url. in the json, the "base domain" of the url is not defined - eg only the part of the path after 'newsletters.fool.com' and 'www.fool.com'. 
			# so based on the service, we decide what base domain to use. this is
			# so that the user can copy-paste a complete url
			article_url = None
			if article_json['legacy_uri']:
				content_base_url = 'newsletters.fool.com'
				if service_slug == 'usmf_free':
					continue
				article_url = content_base_url + article_json['legacy_uri']
			else:
				# for some reason, we couldn't figure out the 'legacy_uri' (essentially, the article's url)
				# without the url, let's say that the article is not worthwhile to SOL.
				print 'could not find legacy_uri'
				continue
			
			# this url & ticker combo should exist only once in our set of Article objects.
			# if the combo already exists, we won't introduce this article for that ticker.
			url_matches = Article.objects.filter(url=article_url, ticker=ticker_match)
			if len(url_matches) >0:
				print 'found duplicate', article_url, ticker_match
				continue

			service = service_matches[0]
			
			publish_date = article_json['publish_at']
			publish_date = publish_date.split('T')[0]

			article = Article()
			article.title = article_json['headline'][:100]
			article.service = service
			article.author = article_json['byline'][:50]
			article.date_pub = datetime.datetime.strptime(publish_date, '%Y-%m-%d')
			article.ticker  = ticker_match
			article.url = article_url
			article.save()

			count_of_articles_added += 1

	return 'number of articles added (one per url/ticker pair): %d' % count_of_articles_added



class Command(BaseCommand):
    help = 'Retrieves from the hydra/napi API the most recent 100 articles across the premium services and creates corresponding Article objects'

    def handle(self, *args, **options):
		print 'starting script'

		event_log = DataHarvestEventLog()
		event_log.data_type = DATA_HARVEST_TYPE_ARTICLES
		event_log.notes = 'running'
		event_log.save()

		script_start_time = datetime.datetime.now()
		try:
			status_message = get_articles()
			log_notes = status_message
		except Exception as e:
			print "error getting articles.", str(e)
			log_notes = str(e)

		script_end_time = datetime.datetime.now()
		total_seconds = (script_end_time - script_start_time).total_seconds()

		print 'time elapsed: %d seconds' %  total_seconds

		event_log.notes = log_notes
		event_log.save()

		print 'finished script'