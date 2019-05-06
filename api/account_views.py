from rest_framework import viewsets
from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.prefetch_related('solves')
    serializer_class = AccountSerializer