import kronos
from django.core.management import call_command


# reset status every weekday morning at 9:00 AM
@kronos.register('00 9 * * 1-5')
def reset_alerts():
	try:
		call_command('reset_rule_status')
	except Exception as e:
		print str(e)

# send out alerts on weekdays at 10 minute intervals, 10:05 AM to 4:55PM
@kronos.register('5,15,25,35,45,55 10-16 * * 1-5')
def assess_alerts():
	try:
		call_command('assess_rules')
	except Exception as e:
		print str(e)
