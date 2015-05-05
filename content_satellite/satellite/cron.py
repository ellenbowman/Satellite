import kronos
from django.core.management import call_command


# https://github.com/jgorset/django-kronos
# python manage.py installtasks
# http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/
# http://alvinalexander.com/linux/unix-linux-crontab-every-minute-hour-day-syntax
# http://www.cronchecker.net/  


### articles ------------------
def _update_articles():
	print 'starting cron task for importing articles'
	try:
		call_command('import_articles')
	except Exception as e:
		print str(e)
	print 'finished cron task for importing articles'	

# on weekdays run at 30 minute intervals, 8 AM to 7:30 PM
@kronos.register('0,30 8-19 * * 1-5')
def update_articles_weekdays():
	_update_articles()

# on weekends run at 2 hr intervals, 8 AM to 8 PM
@kronos.register('0 8,10,12,14,16,18,20 * * 6-7')
def update_articles_weekends():
	_update_articles()

# every day sweep for articles at 11:59 PM
@kronos.register('59 23 * * *')
def update_articles_nightly():
	_update_articles()

### end of updating articles ------------------



### ticker performance ----------------
def _update_daily_percent_change():
	try:
		call_command('update_daily_percent_change')
	except Exception as e:
		print str(e)

# every weekday at 9:00 AM, 9:40 AM, 9:45 AM, and 9:50 AM
# the earliest we expect to get values from Yahoo: 9:45. 
# The 9:40 and 9:50 runs are in case Yahoo is early/late.
# We additionally run the task at 9 AM to zero-out values.
@kronos.register('0,40,45,50 9 * * 1-5')
def update_daily_percent_change_market_open():
	_update_daily_percent_change()


# every weekday 10:00AM-4:45PM, at 15 minute intervals.
@kronos.register('0,15,30,45 10-16 * * 1-5')
def update_daily_percent_change_normal_hours():
	_update_daily_percent_change()

### end of updating ticker performance ----------------