from django.shortcuts import render
from django.db.models import Sum, Count
from django.views.generic import TemplateView, View
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
        bad_submissions = BadSubmission.objects.all()
        total_points_available = challenges.aggregate(Sum('points'))['points__sum']
        bad_submissions_number = bad_submissions.count()
        if bad_submissions_number > 0:
            king_of_wrong_id = bad_submissions.values_list('account').annotate(account_count=Count('account')).order_by('-account_count')[0][0]
            king_of_wrong = Account.objects.get(pk=king_of_wrong_id)
        else:
            king_of_wrong = "No one..."

        context['news'] = News.objects.all().order_by('-created_at')
        context['teams_number'] = Account.objects.count()
        context['challenges_number'] = challenges.count()
        context['total_points_available'] = total_points_available if total_points_available else 0
        context['number_bad_submission'] = bad_submissions_number
        context['kings_of_wrong'] = king_of_wrong
        context['settings'] = current_site
        return context


class ScoreboardView(View):

    def get(self, request, *args, **kwargs):
        return render(self.request, 'scoreboard/list.html')
