from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Account
from apps.scoreboard.models import News

from config.config import read_config

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = read_config()
        context['news'] = News.objects.all().order_by('-created_at')
        context['settings'] = current_site 
        return context


class ScoreboardView(ListView):
    model = Account
    template_name = 'scoreboard/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = sorted(Account.objects.all(), key=lambda t: -t.points)
        return context