from django import forms


class DockerActionForm(forms.Form):
    container_id = forms.CharField(max_length=1024)
    action = forms.CharField(max_length=64)


class DockerImageActionForm(forms.Form):
    image_id = forms.CharField(max_length=1024)
    action = forms.CharField(max_length=64)


class ConfigUpdateForm(forms.Form):
    title = forms.CharField(max_length=64)
