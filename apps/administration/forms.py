from django import forms
from apps.scoreboard.utils import get_themes, get_theme


THEME_CHOICES = [(x, x) for x in get_themes()]


class DockerActionForm(forms.Form):
    container_id = forms.CharField(max_length=1024)
    action = forms.CharField(max_length=64)


class DockerImageActionForm(forms.Form):
    image_id = forms.CharField(max_length=1024)
    action = forms.CharField(max_length=64)


class ConfigUpdateForm(forms.Form):
    title = forms.CharField(max_length=64, required=False)
    theme = forms.ChoiceField(choices=THEME_CHOICES, required=False)
