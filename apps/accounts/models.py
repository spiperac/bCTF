import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string

from libs import pagan
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from apps.teams.models import Team


logger = logging.getLogger(__name__)


def create_pagan(sender, instance, created, **kwargs):
    if created:
        avatar_name = str(instance.pk)
        avatar_folder = "{0}/avatars/{1}/".format(settings.MEDIA_ROOT, instance.pk)
        img = pagan.Avatar(inpt=instance.username, hashfun=pagan.SHA512)
        thumbs = [50, 256]
        img.save(thumbs=thumbs, path=avatar_folder, filename=avatar_name)


def notify_registration(sender, instance, created, **kwargs):
    if created:
        print("Sending email...")
        msg_plain = render_to_string('email/registration.txt', {'team_name': instance.username})

        try:
            send_mail(
                'New Registration - bCTF',
                msg_plain,
                settings.EMAIL_HOST_USER,
                [instance.email],
            )
        except Exception as excp:
            print("Error: {0}".format(str(excp)))
            pass


class Account(AbstractUser):
    banned = models.BooleanField(default=False)
    country = CountryField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    @property
    def get_points_dynamic(self):
        sovles_set = self.solves.prefetch_related('challenges')
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
        sorted_list = list(Account.objects.filter(is_active=True).order_by('-points'))
        rank = sorted_list.index(self) + 1
        return rank

    @property
    def number_solved(self):
        return self.solves.count()

    @property
    def get_avatar(self):
        if not self.avatar:
            url = "{0}avatars/{1}/{1}_50.png".format(settings.MEDIA_URL, self.pk)
            return url
        else:
            return self.avatar.url

    @property
    def get_avatar_big(self):
        if not self.avatar:
            url = "{0}avatars/{1}/{1}_256.png".format(settings.MEDIA_URL, self.pk)
            return url
        else:
            return self.avatar.url

    @property
    def get_avatar_medium(self):
        if not self.avatar:
            url = "{0}avatars/{1}/{1}_128.png".format(settings.MEDIA_URL, self.pk)
            return url
        else:
            return self.avatar.url


post_save.connect(create_pagan, sender=Account)
post_save.connect(notify_registration, sender=Account)
