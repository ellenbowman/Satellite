import kronos
from django.core.management import call_command


# send out alerts on weekdays at 10 minute intervals, 9:55 AM to 4:55PM

def _assess_alerts():
	try:
		call_command('assess_rules')
	except Exception as e:
		print str(e)

# 9:55 AM
@kronos.register('55 9 * * 1-5')
def assess_alerts():
	_assess_alerts()

# 10:05 AM to 5:05 PM -- changed to every hour
@kronos.register('5 10-17 * * 1-5')
def assess_alerts():
	_assess_alerts()
