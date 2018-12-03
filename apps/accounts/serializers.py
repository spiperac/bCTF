from django.conf.urls import url, include
from apps.accounts.models import Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    solves = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('pk', 'username', 'email', 'is_staff', 'solves')
