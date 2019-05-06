from django.db import models
from django_countries.fields import CountryField


class Team(models.Model):
    name = models.CharField(max_length=30)
    country = CountryField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    points = models.IntegerField(default=0)

    @property
    def rank(self):
        sorted_list = list(Team.objects.filter(banned=False).order_by('-points'))
        rank = sorted_list.index(self) + 1
        return rank

    @property
    def number_solved(self):
        return self.solves.count()
