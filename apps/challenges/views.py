import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, FormView, View
from apps.challenges.models import Challenge, Category, Solves
from apps.challenges.forms import SubmitFlagForm


class ChallengesListView(ListView):
    model = Challenge
    context_object_name = 'challenges'
    template_name = 'scoreboard/list_challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['solved_by_user'] = Solves.objects.filter(account=self.request.user.pk).values_list('challenge', flat=True)
        context['solves'] = Solves.objects.all()
        return context

class SubmitFlagView(FormView):
    form_class = SubmitFlagForm
    template_name = 'scoreboard/challenge.html'

    def get_context_data(self, **kwargs):
        context = super(SubmitFlagView, self).get_context_data(**kwargs)
        context['challenge'] = Challenge.objects.get(pk=self.kwargs['pk'])
        context['solvers'] = Solves.objects.filter(challenge=context['challenge'])
        context['solved_by_user'] = Solves.objects.filter(account=self.request.user.pk).values_list('challenge', flat=True)
        return context
        
    def form_valid(self, form):
        challenge_id = form.cleaned_data['challenge_id']
        flag = form.cleaned_data['flag']
        print(challenge_id)
        print(flag)
        challenge = Challenge.objects.get(pk=challenge_id)

        if Solves.objects.filter(challenge=challenge, account=self.request.user).count() == 0:
            if flag in challenge.flag_set.all().values_list('text', flat=True):
                new_solve = Solves.objects.create(
                    challenge=challenge,
                    account=self.request.user,
                )
                return render(self.request, 'scoreboard/flag_success.html', {'challenge_id': challenge_id})
            else:
                return render(self.request, 'scoreboard/flag_success.html', {'challenge_id': challenge_id})
        else:
            return render(self.request, 'scoreboard/flag_success.html', {'challenge_id': challenge_id})
        
 