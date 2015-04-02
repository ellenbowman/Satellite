# find the recent articles for each ticker
# use the 'hydra' api written by Chris Wisecarver
# what does the json look like? here's a sample: https://hydra.fool.com/api/secure/content/

import urllib
import json
import datetime

from models import Article, Ticker, Service


script_start_time = datetime.datetime.now()

BASE_HYDRA_URL = 'https://hydra.fool.com/api/secure/content/query/?stop=20&format=json&service_ids=1081,1069,1502,1451,1371,1321,1255,1228,1128,1066,1062,1048,1008&instrument_ids='

for ticker in Ticker.objects.all().order_by('ticker_symbol'):
	
	print ticker.ticker_symbol

	instrument_id = ticker.instrument_id

	url = BASE_HYDRA_URL + str(instrument_id)
	response = urllib.urlopen(url).read()
	try:
		json_response = json.loads(response)
	except:
		print 'Error processing ' + url
		continue

	if len(json_response) == 1:
		# this means we didn't get results for this ticker;
		# let's not bother trying to process the articles
		continue

	# let's get the first 15 items in the list. 
	count_of_articles_for_this_ticker = 0
	for article_json in json_response:

		if count_of_articles_for_this_ticker >=15:
			break

		article = Article()
		article.title = article_json['headline'][:100]
		
		# examples of values we expect in ['service']['slug']: 'hidden_gems','stock_advisor','supernova'
		# we need to have corresponding Service records
		service_slug = article_json['service']['slug']
		# find those corresponding Service records. in practice, we should get at most 1 match
		services = Service.objects.filter(name=service_slug)
		if len(services)==0:
			# if we don't find a match, then assume it's a usmf article
			print 'no match for service', service_slug
			continue
		else:
			service = services[0]
		article.service = service

		# assign the url. in the json, the "base domain" of the url is not defined - eg only the part of the path after 'newsletters.fool.com' and 'www.fool.com'. 
		# so based on the service, we decide what base domain to use. this is
		# so that the user can copy-paste a complete url
		if article_json['legacy_uri']:
			content_base_url = 'newsletters.fool.com'
			if service_slug == 'usmf_free':
				continue
			article.url = content_base_url + article_json['legacy_uri']
			url_matches = Article.objects.filter(url=article.url, ticker=ticker)
			if len(url_matches) >0:
				print 'found duplicate', article.url
				continue


		article.author = article_json['byline'][:50]
		publish_date = article_json['publish_at']
		publish_date = publish_date.split('T')[0]
		article.date_pub = datetime.datetime.strptime(publish_date, '%Y-%m-%d')

		article.ticker  = ticker
		
		article.save()

		count_of_articles_for_this_ticker += 1

script_end_time = datetime.datetime.now()
total_seconds = (script_end_time - script_start_time).total_seconds()
print 'time elapsed: %d seconds' %  total_seconds