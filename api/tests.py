import string
import random
import json
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import Account

class APITest(TestCase):

    def setUp(self):
        for x in range(0,9):
            team_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            new_account = Account.objects.create(
                username=team_name,
                email="{0}@gmail.com".format(team_name),
            )
            new_account.set_password(team_name)
            new_account.save()

        self.login_account = Account.objects.create(
            username="hacker",
            email="hacker@hackerland.com"
        )
        self.login_account.set_password("hacker123")
        self.login_account.save()

    def login_as_admin(self):
        client = Client()
        response = client.login(username=self.login_account.username, password="hacker123")
        self.assertTrue(response)
        return client

    def test_teams_endpoint(self):
        teams = Account.objects.all().count()
        self.assertEqual(teams, 10)
    
    def test_scores_endpoint(self):
        client = self.login_as_admin()
        response = client.get(reverse('api:score'))
        self.assertEqual(response.status_code, 200)
        scores = response.json()
        scores_length = len(scores['ranks'])
        num_of_accounts = Account.objects.all().count()
        self.assertEqual(scores_length, num_of_accounts)       

        for score in scores['ranks']:
            self.assertEqual(score['points'], 0)
    
    def test_top10_endpoint(self):
        client = self.login_as_admin()
        response = client.get(reverse('api:top'))
        self.assertEqual(response.status_code, 200)
        top = response.json()
        top_length = len(top['ranks'])
        self.assertEqual(top_length, 0)       

    def test_events(self):
        client = self.login_as_admin()
        response = client.get(reverse('api:events'))
        self.assertEqual(response.status_code, 200)

    def test_teams(self):
        client = self.login_as_admin()
        response = client.get(reverse('api:teams'))
        self.assertEqual(response.status_code, 200)
        teams = response.json()