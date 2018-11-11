from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class Account(AbstractUser):
    banned = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def points(self):
        if self.solves_set.all().count() > 0:
            points = self.solves_set.all().aggregate(total_points=models.Sum('challenge__points'))
            if points is None:
                points = 0
                return points
            else:
                return points['total_points']
        else:
            points = 0
            return points

    def rank(self):
        pass
