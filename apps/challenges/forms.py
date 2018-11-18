from django import forms
from apps.challenges.models import Category


class SubmitFlagForm(forms.Form):
    challenge_id = forms.IntegerField()
    flag = forms.CharField(max_length=1024)


class NewChallengeForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea())
    points = forms.IntegerField()
    flag = forms.CharField(max_length=1024)
