import string
import random
from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import Account
from apps.challenges.models import Category, Challenge, Flag, Solves


categories_list = [
    'web',
    'pwn',
    'crypto',
    'forensic',
    'reversing',
    'recon',
    'misc'
]

class Command(BaseCommand):
    help = 'Populates test database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('team_size', type=int)
        parser.add_argument('chall_size', type=int)
        parser.add_argument('solves_size', type=int)

    def create_teams(self, size):
        for x in range(0, size):
                team_name = "team" + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
                new_account = Account.objects.create(
                    username=team_name,
                    email="{0}@gmail.com".format(team_name),
                )
                new_account.set_password(team_name)
                new_account.save()

    def create_categories(self):
        for category in categories_list:
            if Category.objects.filter(name=category).count() == 0:
                Category.objects.create(
                    name=category
               )

    def create_challenges(self, size):

        for x in range(0, size):
            Challenge.objects.create(
                category=Category.objects.get(name=random.choice(categories_list)),
                name=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)),
                description=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + ' ' + string.digits) for _ in range(40)),
                points=''.join(random.choice(string.digits) for _ in range(3))
            )

    def create_solves(self, size):
        for x in range(0, size):
            challenge = random.choice(Challenge.objects.all())
            account = random.choice(Account.objects.all())
            Solves.objects.create(
                challenge=challenge,
                account=account
            )

    def handle(self, *args, **options):
        self.create_categories()
        self.create_teams(options['team_size'])
        self.create_challenges(options['chall_size'])
        self.create_solves(options['solves_size'])