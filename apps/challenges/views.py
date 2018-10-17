import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.challenges.models import Challenge, Category, Solves
from apps.challenges.forms import SubmitFlagForm


class ChallengesListView(LoginRequiredMixin, ListView):
    model = Challenge
    context_object_name = 'challenges'
    template_name = 'challenge/list_challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['solved_by_user'] = Solves.objects.filter(account=self.request.user.pk).values_list('challenge', flat=True)
        context['solves'] = Solves.objects.all()
        return context

class SubmitFlagView(LoginRequiredMixin, FormView):
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
                new_solve = Solves.objects.create(
                    challenge=challenge,
                    account=self.request.user,
                )
                return render(self.request, 'challenge/flag_success.html', {'challenge': challenge})
            else:
                return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Wrong flag!'})
        else:
            return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Already solved!'})
        
 