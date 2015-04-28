from django import forms

# class NotesForm(forms.Form):
#    edit_notes = forms.CharField(label='Edit ticker notes', max_length=1000, widget=forms.Textarea)

class NotesForm(forms.Form):
    service = forms.CharField()
    premium_coverage = forms.CharField(widget=forms.Textarea)
    dotcom_coverage = forms.CharField(widget=forms.Textarea)