import logging
from plugins import pagan
from PIL import Image
from hashlib import md5
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db.models.signals import post_save


logger = logging.getLogger(__name__)


def create_pagan(sender, instance, created, **kwargs):
    if created:
        avatar_name = str(instance.pk)
        avatar_folder = "{0}/avatars/{1}/".format(settings.MEDIA_ROOT, instance.pk)
        img = pagan.Avatar(inpt=instance.username, hashfun=pagan.SHA512)
        thumbs = [50, 256]
        img.save(thumbs=thumbs, path=avatar_folder, filename=avatar_name)

        


class Account(AbstractUser):
    banned = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    @property
    def get_points_dynamic(self):
        sovles_set = self.solves_set.prefetch_related('challenges')
        if sovles_set.count() > 0:
            points = sovles_set.values("challenge__points").aggregate(total_points=models.Sum('challenge__points'))
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
            url = "{0}avatars/{1}/{1}_50.png".format(settings.MEDIA_URL, self.pk)
            return url
        else:
            return self.avatar.url


post_save.connect(create_pagan, sender=Account)
