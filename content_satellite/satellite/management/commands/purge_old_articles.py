'''
purge articles older than 100 days
'''
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from satellite.models import Article

max_age_in_days = 100

class Command(BaseCommand):
    help = 'Deletes articles older than 100 days'

    def handle(self, *args, **options):
    	print 'starting script'

        print 'how many articles?', len(Article.objects.all())
        date_threshold = (datetime.today() - timedelta(days=max_age_in_days)).date()
    	all_articles = Article.objects.all()


    	for art in all_articles:
            if art.date_pub < date_threshold:
                print "deleting ", art.url
                art.delete()

    	print 'how many articles now?', len(Article.objects.all())
    	print 'finished script'
