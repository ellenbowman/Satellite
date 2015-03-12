# find the recent articles for each ticker
# use the 'hydra' api written by Chris Wisecarver
# what does the json look like? here's a sample: https://hydra.fool.com/api/secure/content/

import urllib
import json
import datetime

from models import Article, Ticker, Service


BASE_HYDRA_URL = 'https://hydra.fool.com/api/secure/content/query/?stop=5&format=json&instrument_ids='


for ticker in Ticker.objects.all():
	
	print ticker.ticker_symbol

	instrument_id = ticker.instrument_id

	url = BASE_HYDRA_URL + str(instrument_id)
	response = urllib.urlopen(url).read()
	json_response = json.loads(response)

	if len(json_response) == 1:
		# this means we didn't get results for this ticker;
		# let's not bother trying to process the articles
		continue

	# let's get the first 10 items in the list. 
	for jr in json_response[:10]:
		article = Article()
		article.title = jr['headline']
		
		# examples of values we expect in ['service']['slug']: 'hidden_gems','stock_advisor','supernova'
		# we need to have corresponding Service records
		service_slug = jr['service']['slug']
		# find those corresponding Service records. in practice, we should get at most 1 match
		services = Service.objects.filter(name=service_slug)
		if len(services)==0:
			# if we don't find a match, then assume it's a usmf article
			service  = Service.objects.get(name='usmf_free')
		else:
			service = services[0]
		article.service = service

		# assign the url. in the json, the "base domain" of the url is not defined - eg only the part of the path after 'newsletters.fool.com' and 'www.fool.com'. 
		# so based on the service, we decide what base domain to use. this is
		# so that the user can copy-paste a complete url
		if jr['legacy_uri']:
			content_base_url = 'newsletters.fool.com'
			if service_slug == 'usmf_free':
				content_base_url = 'www.fool.com'
			article.url = content_base_url + jr['legacy_uri']


		article.author = jr['byline']
		publish_date = jr['publish_at']
		publish_date = publish_date.split('T')[0]
		article.date_pub = datetime.datetime.strptime(publish_date, '%Y-%m-%d')

		article.ticker  = ticker
		
		article.save()
