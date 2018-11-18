import json
from django.shortcuts import render
from django.http import JsonResponse

from apps.accounts.models import Account
from apps.challenges.models import Solves, Challenge

def scores(request):
    if request.method == 'GET':
        response = {}
        response['ranks'] = []
        number_challenges = Challenge.objects.count()
        
        accounts_scored = Account.objects.prefetch_related('solves_set').filter(points__gt=0).filter(is_active=True).order_by('-points')

        for (rank, account) in enumerate(accounts_scored, start=1):
            team = {}
            team['id'] = account.pk
            team['name'] = account.username
            team['country'] = account.country.flag_css
            team['points'] = account.points
            team['precentage'] = str(round((account.number_solved * 100) / number_challenges if account.number_solved or number_challenges else 0, 2))
            team['avatar'] = account.get_avatar
            team['rank'] = rank
            response['ranks'].append(team)
        
        return JsonResponse(response)

def top_scores(request):
    if request.method == 'GET':
        response = {}
        response['ranks'] = {}
        
        if Solves.objects.count() > 0:
            for (rank, account) in enumerate(Account.objects.prefetch_related('solves_set').order_by('-points')[:10], start=1):
                team = {}
                team['id'] = account.pk
                team['name'] = account.username
                team['solves'] = []

                for solve in account.solves_set.select_related('challenge').iterator():
                    chall = {}
                    chall['chal'] = solve.challenge_id
                    chall['team'] = account.pk
                    chall['time'] = int(solve.created_at.timestamp())
                    chall['value'] = solve.challenge.points
                    team['solves'].append(chall)

                response['ranks'].update({rank: team})

            return JsonResponse(response)
        else:
            return JsonResponse(response)

def events(request):
    if request.method == 'GET':
        response = {}
        response['events'] = []

        latest_events = Solves.objects.prefetch_related('account').prefetch_related('challenge').order_by('-created_at')[:5]
        for event in latest_events:
            new_event = {}
            new_event['team'] = event.account.username
            new_event['team_id'] = event.account_id
            new_event['challenge'] = event.challenge.name
            new_event['time'] = event.created_at.strftime("%Y-%m-%d %H:%M")
            response['events'].append(new_event)
        
        return JsonResponse(response)

def teams(request):
    if request.method == 'GET':
        response = {}
        response['teams'] = []
        
        teams = Account.objects.all().order_by('date_joined')
        for team in teams:
            new_team = {}
            new_team['name'] = team.username
            
            response['teams'].append(new_team)

        return JsonResponse(response)
