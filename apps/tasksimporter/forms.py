from django import forms
from django.core.validators import FileExtensionValidator


class ImportTasksForm(forms.Form):
    zip_file = forms.FileField(validators=[FileExtensionValidator(['zip'])])
