from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.hashers import check_password
from apps.accounts.models import Account
from apps.accounts.forms import AccountCreationForm, AccountChangeForm
from apps.challenges.models import Solves, FirstBlood, Challenge


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
        first_bloods = FirstBlood.objects.prefetch_related('challenge').filter(account=self.object.pk)
        solves = Solves.objects.prefetch_related('challenge').filter(account=self.object.pk)

        context['solved'] = solves if solves else 0
        context['first_bloods'] = first_bloods if first_bloods else 0
        context['solved_stats'] = [solves.count(), Challenge.objects.count() - solves.count()]
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AccountChangeForm
    template_name = 'account/update.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()
