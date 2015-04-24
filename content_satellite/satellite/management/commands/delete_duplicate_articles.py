'''
what makes an article worth keeping?
for a given title, url, service, & ticker combination, we want at most one article. 
let's say these features make up an article's "profile".
this script deletes articles that have a profile already accounted for in Satellite.
'''
from django.core.management.base import BaseCommand, CommandError

from satellite.models import Article

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

    	all_articles = Article.objects.all()
    	print 'how many articles?', len(all_articles)

    	article_profiles_already_processed = set()
    	articles_to_delete = set()

    	for art in all_articles:
    		profile = (art.title, art.url, art.service.name, art.ticker.instrument_id)

    		if profile in article_profiles_already_processed:
    			articles_to_delete.add(art)
    		else:
    			article_profiles_already_processed.add(profile)

    	print 'how many unique article profiles?', len(article_profiles_already_processed)
    	print 'how many articles to delete?', len(articles_to_delete)

    	for art_to_delete in articles_to_delete:
			art.delete()
    	all_articles = Article.objects.all()
    	
    	print 'how many articles now?', len(all_articles)
    	print 'finished script'






