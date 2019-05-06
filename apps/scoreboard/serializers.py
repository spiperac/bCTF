from django.conf.urls import url, include
from apps.accounts.models import Account
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField


class ScoreboardSerializer(CountryFieldMixin, serializers.ModelSerializer):
    country = CountryField(country_dict=True)

    class Meta:
        model = Account
        fields = ('pk', 'username', 'points', 'country')
