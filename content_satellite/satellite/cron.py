import kronos
from django.core.management import call_command


# https://github.com/jgorset/django-kronos
# python manage.py installtasks
# http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/
# http://alvinalexander.com/linux/unix-linux-crontab-every-minute-hour-day-syntax

# run every day between 7AM and 8PM, at 20 minute intervals
@kronos.register('00,20,40 * * * *')
def update_articles():
	print 'starting cron task for importing articles'
	try:
		call_command('import_articles')
	except Exception as e:
		print str(e)
	print 'finished cron task for importing articles'	



# every weekday 8AM-5PM, at 20 minute intervals
@kronos.register('00,20,40 08-17 * * 1-5')
def update_daily_percent_change():
	print 'starting cron task for updating daily percent change'
	try:
		call_command('update_daily_percent_change')
	except Exception as e:
		print str(e)
	print 'finished cron task for updating daily percent change'
