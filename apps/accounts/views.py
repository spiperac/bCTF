from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from apps.accounts.models import Account
from apps.accounts.forms import AccountCreationForm

class RegistrationView(CreateView):
    form_class = AccountCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('scoreboard:home'))
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)