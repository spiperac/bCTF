from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from apps.accounts.models import Account
from apps.accounts.forms import AccountCreationForm
from apps.challenges.models import Solves, FirstBlood


class RegistrationView(CreateView):
    form_class = AccountCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('scoreboard:home'))
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)


class ProfileView(DetailView):
    model = Account
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solved'] = Solves.objects.filter(account=self.object.pk)
        context['first_bloods'] = FirstBlood.objects.filter(account=self.object.pk)
        return context
