from rest_framework import viewsets
from apps.accounts.models import Account
from apps.scoreboard.serializers import ScoreboardSerializer


class ScoreboardViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-points')
    serializer_class = ScoreboardSerializer