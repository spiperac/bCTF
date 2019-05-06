import random
from libs import pagan
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.accounts.models import Account


class Command(BaseCommand):
    help = 'Generates avatars for all users in db'

    def generate_avatars(self):
        for account in Account.objects.all():
            avatar_name = str(account.pk)
            avatar_folder = "{0}/avatars/{1}/".format(settings.MEDIA_ROOT, account.pk)
            img = pagan.Avatar(inpt=account.username, hashfun=pagan.SHA512)
            thumbs = [50, 256]
            img.save(thumbs=thumbs, path=avatar_folder, filename=avatar_name)

    def handle(self, *args, **options):
        self.generate_avatars()
