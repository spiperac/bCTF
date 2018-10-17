import json
from django.shortcuts import render
from django.http import JsonResponse

from apps.accounts.models import Account

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
