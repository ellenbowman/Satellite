from django import forms

class NotesForm(forms.Form):
    edit_notes = forms.CharField(label='Edit ticker notes', max_length=1000, widget=forms.Textarea)