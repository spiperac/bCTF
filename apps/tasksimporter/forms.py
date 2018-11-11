from django import forms

class ImportTasksForm(forms.Form):
    zip_file = forms.FileField()
    