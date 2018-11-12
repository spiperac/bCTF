from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.accounts.models import Account
from django.contrib.auth.hashers import check_password


class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ('username', 'email', 'country', 'password1', 'password2')


class AccountChangeForm(forms.ModelForm):
    email = forms.CharField(max_length=1024)
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Account
        fields = ('email', 'country', 'avatar', )

    def clean(self):
        cleaned_data = super(AccountChangeForm, self).clean()
        current_password = cleaned_data.get('current_password')
        if not check_password(current_password, self.instance.password):
            self.add_error('current_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(AccountChangeForm, self).save(commit)
        if self.data['new_password']:
            user.set_password(self.data['new_password'])
        if commit:
            user.save()
        return user
