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


class FlagAddForm(forms.Form):
    challenge_id = forms.IntegerField()
    flag = forms.CharField(max_length=1024)


class FlagDeleteForm(forms.Form):
    flag = forms.IntegerField()


class HintAddForm(forms.Form):
    challenge_id = forms.IntegerField()
    hint = forms.CharField(max_length=1024)


class HintDeleteForm(forms.Form):
    hint = forms.IntegerField()


class AttachmentAddForm(forms.Form):
    challenge_id = forms.IntegerField()
    data = forms.FileField()


class AttachmentDeleteForm(forms.Form):
    attachment = forms.IntegerField()
