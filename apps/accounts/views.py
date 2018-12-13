import json
from itertools import accumulate
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from ratelimit.mixins import RatelimitMixin
from django.views.generic import CreateView, View, UpdateView
from apps.accounts.models import Account
from apps.accounts.forms import AccountCreationForm, AccountChangeForm
from apps.challenges.models import Solves, FirstBlood, Challenge


class RegistrationView(CreateView):
    form_class = AccountCreationForm
    success_url = reverse_lazy('login')

    def get_template_names(self):
        return list(['templates/registration/signup.html'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('scoreboard:home'))
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)


class Login(RatelimitMixin, LoginView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_method = 'POST'
    ratelimit_block = True
    redirect_authenticated_user = True

    def get_template_names(self):
        return list(['templates/registration/login.html'])


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        self.object = get_object_or_404(Account, pk=self.kwargs['pk'])
        first_bloods = FirstBlood.objects.prefetch_related('challenge').filter(account=self.object.pk)
        solves = Solves.objects.prefetch_related('challenge').prefetch_related('challenge__category').filter(account=self.object.pk)
        total_points_available = Challenge.objects.aggregate(Sum('points'))['points__sum']
        accumulated_scores = list(accumulate(list([x.challenge.points for x in solves])))
        times = list([x.created_at.timestamp() for x in solves])
        axes_data = []
        for time, score in zip(times, accumulated_scores):
            data = {}
            data["x"] = time * 1000
            data["y"] = score
            axes_data.append(data)

        dataset = {}
        dataset["label"] = self.object.username
        dataset["showLine"] = "true"
        dataset["data"] = axes_data
        dataset["backgroundColor"] = "greenyellow"
        dataset["borderColor"] = "greenyellow"
        dataset["showLine"] = "true"
        dataset["pointRadius"] = 5
        dataset["pointHoverRadius"] = 5
        dataset["fill"] = "false"

        context['object'] = self.object
        context['solved'] = solves if solves else 0
        context['rank'] = self.object.rank
        context['progress'] = str(round((self.object.points * 100) / total_points_available if self.object.points or total_points_available else 0, 2))
        context['first_bloods'] = first_bloods if first_bloods else 0
        context['solved_stats'] = [solves.count(), Challenge.objects.count() - solves.count()]
        context['solved_dataset'] = json.dumps(dataset)
        return render(self.request, 'templates/account/profile.html', context=context)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AccountChangeForm

    def get_template_names(self):
        return list(['templates/account/update.html'])

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()
