from django import forms

class TickerNotesForm(forms.Form):
    edit_notes = forms.CharField(label='Edit ticker notes', max_length=1000)
