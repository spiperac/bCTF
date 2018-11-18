import json
import time
from django.shortcuts import render
from django.db.models import Count
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.challenges.models import Challenge, Category, Solves, FirstBlood, BadSubmission, Flag, Attachment
from apps.challenges.forms import SubmitFlagForm, NewChallengeForm
from config.config import read_config


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CtfNotEnded(UserPassesTestMixin):
    def test_func(self):
        cfg = read_config()
        if cfg['ctf']['start_time'] is None or cfg['ctf']['end_time'] is None:
            return True
        elif int(cfg['ctf']['start_time']) < int(time.time()) < int(cfg['ctf']['end_time']):
            return True
        else:
            return False


class ChallengesListView(LoginRequiredMixin, ListView):
    queryset = Challenge.objects.prefetch_related('category').prefetch_related('solves_set').all()
    context_object_name = 'challenges'
    template_name = 'challenge/list_hexagon_challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solves = Solves.objects.prefetch_related('challenge').prefetch_related('account')

        context['categories'] = Category.objects.all()
        context['solved_by_user'] = solves.values_list('challenge', flat=True).filter(account=self.request.user.pk)
        context['solves'] = solves.values("challenge__name").annotate(c=Count('challenge')).order_by('-c')
        context['first_bloods'] = FirstBlood.objects.prefetch_related('account').prefetch_related('challenge')
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
                new_bad_submission = BadSubmission.objects.create(
                    challenge=challenge,
                    account=self.request.user,
                    flag=flag
                )
                return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Wrong flag!'})
        else:
            return render(self.request, 'challenge/challenge.html', {'challenge': challenge, 'solvers': Solves.objects.filter(challenge=challenge), 'error': 'Already solved!'})


class CreateChallengeView(SuccessMessageMixin, LoginRequiredMixin, UserIsAdminMixin, FormView):
    form_class = NewChallengeForm
    template_name = 'challenge/new_challenge.html'
    success_url = reverse_lazy('administration:ctf')
    success_message = "Challenge %(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super(CreateChallengeView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        category = form.cleaned_data['category']
        flag = form.cleaned_data['flag']

        new_challenge = Challenge(
            category=category,
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            points=form.cleaned_data['points'],
            visible=True
        )

        new_challenge.save()
        new_flag = Flag(
            challenge=new_challenge,
            text=form.cleaned_data['flag']
        )

        if self.request.FILES:
            files = self.request.FILES.getlist('attachments')
            if files:
                for f in files:
                    new_attachment = Attachment.objects.create(
                        challenge=new_challenge,
                        data=f
                    )

        new_flag.save()
        return super(CreateChallengeView, self).form_valid(form)
