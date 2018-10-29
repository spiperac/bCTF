from django import forms


class FlagAddForm(forms.Form):
    challenge_id = forms.IntegerField()
    flag = forms.CharField(max_length=1024)

class HintAddForm(forms.Form):
    challenge_id = forms.IntegerField()
    hint = forms.CharField(max_length=1024)

class HintDeleteForm(forms.Form):
    hint = forms.IntegerField()
