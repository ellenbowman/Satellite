from django import forms
from models import Service

# https://docs.djangoproject.com/en/1.7/ref/forms/api/
# https://docs.djangoproject.com/en/1.7/ref/forms/fields/#django.forms.ModelMultipleChoiceField	

# class NotesForm(forms.Form):
#    edit_notes = forms.CharField(label='Edit ticker notes', max_length=1000, widget=forms.Textarea)

class NotesForm(forms.Form):
    service = forms.CharField()
    premium_coverage = forms.CharField(widget=forms.Textarea)
    dotcom_coverage = forms.CharField(widget=forms.Textarea)

class ArticlesFilterForm(forms.Form):
	tickers = forms.CharField(required=False)
	
	services = forms.ModelMultipleChoiceField(
		widget=forms.SelectMultiple(attrs={'class': 'service-select-tall'}),
		queryset=Service.objects.all().order_by('pretty_name'), 
		required=False)	
	
	