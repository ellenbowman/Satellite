from django import forms
from push_notifications.models import NotificationSubscriber


class SubscriberForm(forms.ModelForm):
	class Meta:
		model = NotificationSubscriber
