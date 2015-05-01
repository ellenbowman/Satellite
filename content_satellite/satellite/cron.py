import kronos
from django.core.management import call_command


# https://github.com/jgorset/django-kronos
# python manage.py installtasks
# http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/
# http://alvinalexander.com/linux/unix-linux-crontab-every-minute-hour-day-syntax
# http://www.cronchecker.net/  


# runs at 30 minute intervals, every day, 7 AM to 8 PM
@kronos.register('0,30 7-20 * * *')
def update_articles():
	print 'starting cron task for importing articles'
	try:
		call_command('import_articles')
	except Exception as e:
		print str(e)
	print 'finished cron task for importing articles'	



# every weekday 10:00AM-5PM, at 15 minute intervals
@kronos.register('0,15,30,45 10-17 * * 1-5')
def update_daily_percent_change():
	print 'starting cron task for updating daily percent change'
	try:
		call_command('update_daily_percent_change')
	except Exception as e:
		print str(e)
	print 'finished cron task for updating daily percent change'
