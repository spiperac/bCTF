from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView
from apps.accounts.models import Account
from apps.accounts.forms import AccountCreationForm, AccountChangeForm
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

class AccountUpdateView(UpdateView):
    form_class = AccountChangeForm
    model = Account
    template_name = 'account/update.html'

    def get(self, request, **kwargs):
        self.object = Account.objects.get(pk=self.request.user.pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())