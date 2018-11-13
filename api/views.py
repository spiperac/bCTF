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
        
        accounts_scored = [account for account in Account.objects.prefetch_related('solves_set').iterator() if account.points > 0 and account.is_active is True]

        for (rank, account) in enumerate(sorted(accounts_scored, key=lambda t: -t.points), start=1):
            team = {}
            team['id'] = account.pk
            team['name'] = account.username
            team['country'] = account.country.flag
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
        
        if Solves.objects.all().count() > 0:
            for (rank, account) in enumerate(sorted(Account.objects.all(), key=lambda t: -t.points)[:10], start=1):
                team = {}
                team['id'] = account.pk
                team['name'] = account.username
                team['solves'] = []
                solved = account.solves_set.all()

                for solve in solved:
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

        latest_events = Solves.objects.all().order_by('-created_at')[:5]
        for event in latest_events:
            new_event = {}
            new_event['team'] = event.account.username
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
