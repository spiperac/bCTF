import json
from django.shortcuts import render
from django.http import JsonResponse

from apps.accounts.models import Account
from apps.challenges.models import Solves

def scores(request):
    if request.method == 'GET':
        response = {}
        response['ranks'] = []
        for (rank, account) in enumerate(sorted(Account.objects.all(), key=lambda t: -t.points), start=1):
            team = {}
            team['id'] = account.pk
            team['name'] = account.username
            team['points'] = account.points
            team['rank'] = rank
            response['ranks'].append(team)
        
        return JsonResponse(response)

def top_scores(request):
    if request.method == 'GET':
        response = {}
        response['ranks'] = {}

        if Solves.objects.all().count() > 0:
            for (rank, account) in enumerate(sorted(Account.objects.all(), key=lambda t: -t.points)[:10], start=1):
                team = {}
                team['id'] = account.pk
                team['name'] = account.username
                team['solves'] = []
                solved = account.solves_set.all()

                for solve in solved:
                    chall = {}
                    chall['chal'] = solve.challenge.id
                    chall['team'] = account.pk
                    chall['time'] = int(solve.created_at.timestamp())
                    chall['value'] = solve.challenge.points
                    team['solves'].append(chall)

                response['ranks'].update({rank: team})

            return JsonResponse(response)
        else:
            return JsonResponse(response)