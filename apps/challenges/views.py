import json
import time
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.challenges.models import Challenge, Category, Solves, FirstBlood
from apps.challenges.forms import SubmitFlagForm
from apps.challenges.decorators import ctf_ended
from config.config import read_config


class CtfNotEnded(UserPassesTestMixin):
        def test_func(self):
                cfg = read_config()
                if int(cfg['ctf']['start_time']) < int(time.time()) < int(cfg['ctf']['end_time']):
                        return True
                else:
                        return False


class ChallengesListView(CtfNotEnded, LoginRequiredMixin, ListView):
    model = Challenge
    context_object_name = 'challenges'
    template_name = 'challenge/list_hexagon_challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['solved_by_user'] = Solves.objects.filter(account=self.request.user.pk).values_list('challenge', flat=True)
        context['solves'] = Solves.objects.all()
        context['first_bloods'] = FirstBlood.objects.all()
        return context

class SubmitFlagView(CtfNotEnded, LoginRequiredMixin, FormView):
    form_class = SubmitFlagForm
    template_name = 'challenge/challenge.html'

    def get_context_data(self, **kwargs):
        context = super(SubmitFlagView, self).get_context_data(**kwargs)
        context['challenge'] = Challenge.objects.get(pk=self.kwargs['pk'])
        context['solvers'] = Solves.objects.filter(challenge=context['challenge'])
        context['solved_by_user'] = Solves.objects.filter(account=self.request.user.pk).values_list('challenge', flat=True)
        return context
        
    def form_valid(self, form):
        challenge_id = form.cleaned_data['challenge_id']
        flag = form.cleaned_data['flag']
        challenge = Challenge.objects.get(pk=challenge_id)

        if Solves.objects.filter(challenge=challenge, account=self.request.user).count() == 0:
            if flag in challenge.flag_set.all().values_list('text', flat=True):
                if Solves.objects.filter(challenge=challenge).count() == 0:
                    new_first_blood = FirstBlood.objects.create(
                        challenge=challenge,
                        account=self.request.user,                       
                    )

                new_solve = Solves.objects.create(
                    challenge=challenge,
                    account=self.request.user,
                )
                return render(self.request, 'challenge/flag_success.html', {'challenge': challenge})
            else:
                return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Wrong flag!'})
        else:
            return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Already solved!'})
        
 