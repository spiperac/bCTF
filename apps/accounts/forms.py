from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.accounts.models import Account

class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('username', 'email')

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('username', 'email')