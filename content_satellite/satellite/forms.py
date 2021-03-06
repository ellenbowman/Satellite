from django import forms
from models import Service, Ticker, Article, CoverageType
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

class TickerForm(forms.ModelForm):
	class Meta:
		model = Ticker
		fields = ('tier','tier_status', 'promised_coverage', 'notes',)

class NotesForm(forms.ModelForm):
	class Meta:
		model = Ticker
		fields = ('notes',)
		

class CoverageTypeForm(forms.ModelForm):
	class Meta:
		model = CoverageType
		fields = ('author', 'coverage_type')
	