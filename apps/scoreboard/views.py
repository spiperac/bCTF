from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Account
from apps.scoreboard.models import News
from apps.challenges.models import Challenge, BadSubmission
from config.config import read_config


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = read_config()
        challenges = Challenge.objects.all()
        context['news'] = News.objects.all().order_by('-created_at')
        context['teams_number'] = Account.objects.count()
        context['challenges_number'] = challenges.count()
        context['total_points_available'] = challenges.aggregate(Sum('points'))['points__sum']
        context['number_bad_submission'] = BadSubmission.objects.count()
        context['settings'] = current_site
        return context


class ScoreboardView(ListView):
    model = Account
    template_name = 'scoreboard/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = sorted(Account.objects.all(), key=lambda t: -t.points)
        return context
