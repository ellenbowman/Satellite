from django import forms

class FeedbackForm(forms.Form):

    name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True, max_length=30)
    comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': 55, 'rows': 5}), max_length=500)
