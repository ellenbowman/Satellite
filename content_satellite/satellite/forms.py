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

class AnalystsForm(forms.Form):

	all_authors = [a.author for a in Article.objects.all()[:20]]
	individual_authors = [a.split(" and")[0] for a in all_authors]
	duplicate_authors = set()
	very_individual_authors = []
	for a in individual_authors:
		if a not in duplicate_authors:
			duplicate_authors.add(a)
			very_individual_authors.append(a)
	very_individual_authors = sorted(very_individual_authors)

	AUTHOR_CHOICES = [[a, a] for a in very_individual_authors]
	print AUTHOR_CHOICES

	analyst1 = forms.ChoiceField(
		choices=BLANK_CHOICE_DASH + list(AUTHOR_CHOICES),
		required=False,
		)
	analyst2 = forms.ChoiceField(
		choices=BLANK_CHOICE_DASH + list(AUTHOR_CHOICES),
		required=False,
		)
	analyst3 = forms.ChoiceField(
		choices=BLANK_CHOICE_DASH + list(AUTHOR_CHOICES),
		required=False,
		)







