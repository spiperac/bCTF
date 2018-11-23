from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from apps.accounts.models import Account
from apps.challenges.models import Challenge


class CTFTimeView(View):
	def get(self, request, *args, **kwargs):
		response = {}
		response['tasks'] = [x.name for x in Challenge.objects.all()]
		response['standings'] = []
		accounts_scored = Account.objects.filter(points__gt=0).filter(is_active=True).order_by('-points')

		for (rank, account) in enumerate(accounts_scored, start=1):
			team = {}
			team['pos'] = rank
			team['team'] = account.username
			team['score'] = account.points

			response['standings'].append(team)

		return JsonResponse(response)
