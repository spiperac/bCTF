from django import forms


class InstallForm(forms.Form):
    ctf_name = forms.CharField(max_length=1024)
    admin_username = forms.CharField(max_length=128)
    admin_email = forms.EmailField()
    admin_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
