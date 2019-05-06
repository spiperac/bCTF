from rest_framework import viewsets
from apps.challenges.models import Solves
from apps.challenges.serializers import SolvesSerializer


class SolvesViewSet(viewsets.ModelViewSet):
    queryset = Solves.objects.prefetch_related('challenge').prefetch_related('account')
    serializer_class = SolvesSerializer