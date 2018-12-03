from django.conf.urls import url, include
from apps.challenges.models import Solves
from rest_framework import serializers


class SolvesSerializer(serializers.ModelSerializer):
    challenge = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    account = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Solves
        fields = ('pk', 'challenge', 'account', 'created_at')
