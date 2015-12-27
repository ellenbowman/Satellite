from django import forms

class WWTNForm(forms.Form):

    name = forms.CharField(required=True, max_length=30)
    ticker = forms.CharField(required=True, max_length=30)
    wwtn = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': 55, 'rows': 5}), max_length=5000)
