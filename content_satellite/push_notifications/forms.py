from django import forms
from push_notifications.models import NotificationSubscriber


class SubscriberForm(forms.ModelForm):
	class Meta:
		model = NotificationSubscriber
		fields = ('slack_handle','tickers_csv', 'services',)

	def clean_slack_handle(self):
		data = self.cleaned_data['slack_handle']
		if not data.startswith('@') and not data.startswith('#'):
			raise forms.ValidationError("slack handle should start with '@' or '#'")
		if ' ' in data:
			raise forms.ValidationError("slack handle should not contain spaces")
		if len(data) < 3:
			raise forms.ValidationError("this doesn't look like a slack handle")
