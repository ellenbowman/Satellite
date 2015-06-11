from django import forms
from models import Service, Ticker, Article
from django.forms.models import modelformset_factory
from django.db.models.fields import BLANK_CHOICE_DASH

# https://docs.djangoproject.com/en/1.7/ref/forms/api/
# https://docs.djangoproject.com/en/1.7/ref/forms/fields/#django.forms.ModelMultipleChoiceField

class FilterForm(forms.Form):
	TIER_OPTIONS = (
		('core', 'core'),
		('first', 'first'),
		('popular', 'popular'),
		('starter', 'starter'),
		)
	tickers = forms.CharField(required=False)
	notes = forms.CharField(
		widget=forms.Textarea,
		required=False)
	services = forms.ModelMultipleChoiceField(
		queryset=Service.objects.all().order_by('pretty_name'), 
		required=False)
	tier_status = forms.MultipleChoiceField(
		choices=TIER_OPTIONS,
		required=False)

class ContentTypeForm(forms.Form):
	TEN_PERCENT_PROMISE = 1
	FIVE_AND_THREE = 2
	EARNINGS_PREVIEW = 3
	EARNINGS_REVIEW = 4
	RISK_RATING = 5
	COVERAGE_CHOICES = (
		(TEN_PERCENT_PROMISE, '10% Promise'),
		(FIVE_AND_THREE, '5 and 3'),
		(EARNINGS_PREVIEW, 'Earnings Preview'),
		(EARNINGS_REVIEW, 'Earnings Review'),
		(RISK_RATING, 'Risk Rating'),
		)
	content_type = forms.MultipleChoiceField(choices=COVERAGE_CHOICES)




