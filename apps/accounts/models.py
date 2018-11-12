from hashlib import md5
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class Account(AbstractUser):
    banned = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

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

    @property
    def rank(self):
        sorted_list = sorted(Account.objects.filter(is_active=True), key=lambda t: -t.points)
        rank = sorted_list.index(self) + 1
        return rank

    @property
    def number_solved(self):
        return self.solves_set.count()

    @property
    def get_avatar(self):
        if not self.avatar:
                email = str(self.email.strip().lower()).encode('utf-8')
                email_hash = md5(email).hexdigest()
                url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
                return url.format(email_hash, 35)
        else:
            return self.avatar.url
