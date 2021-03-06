import urllib
import urllib2
import json

def post_message_to_slack(message_text='a message from Satellite', channel='#content_satellite', username='Dr. Satellite', icon_emoji=':sol_2:'):
	"""
	message_text: the markup for the message body
	channel: which channel should receive the message

	refs:
	https://slack.zendesk.com/hc/en-us/articles/202009646-Using-channel-group-everyone 
	https://slack.zendesk.com/hc/en-us/articles/202288908-Formatting-your-messages
	https://api.slack.com/docs/formatting
	"""

	url = 'https://hooks.slack.com/services/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'

	payload = {
		'text': message_text,
		'channel': channel,
		'username': username,
		'icon_emoji': icon_emoji,
	}

	params = urllib.urlencode({
		'payload': json.dumps(payload),
	})

	return urllib2.urlopen(url, params).read()
