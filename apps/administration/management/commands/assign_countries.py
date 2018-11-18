import random
from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import Account
from django_countries import countries


class Command(BaseCommand):
    help = 'Populates test database with dummy data'

    def assign_random_countries(self):
        for account in Account.objects.all():
            account.country = random.choice(countries)
            account.save()

    def handle(self, *args, **options):
        self.assign_random_countries()
