from django import forms
from models import Service, Ticker, Article
from django.forms.models import modelformset_factory

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

class SelectAnalystForm(forms.Form):
	"""
	duplicate_authors = set()
	author_list = []
	for a in Article.objects.all():
		if a.author not in duplicate_authors:
			duplicate_authors.add(a.author)
			author_list.append(a.author)
	print author_list
	"""
	analyst = forms.CharField(required=False)









