from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import Account
from apps.challenges.models import Category, Challenge, Flag


class ChallengeTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            username="hacker",
            email="hacker@hackerland.com",
        )

        self.account.set_password("hacker123")
        self.account.save()

        self.test_title = "Challenges TEST"
        category = Category.objects.create(
            name="pwn"
        )

        Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000
        )

    def login_client(self):
        client = Client()
        response = client.post(reverse('login'), {'username': self.account.username, 'password': 'hacker123'})
        self.assertEqual(response.status_code, 302)
        return client

    def test_add_challenge_and_verify_category(self):
        """
        Just verify if challenge is created, and put into correct category
        """
        challenge = Challenge.objects.get(name="pwn1")
        category = Category.objects.get(name="pwn")
        self.assertEqual(challenge.category.name, category.name)

    def test_challenge_list(self):
        """
        Check if challenge actually showd up on challenges list page.
        """
        client = self.login_client()
        challenge = Challenge.objects.get(name="pwn1")

        response = client.get(reverse('challenge:list-challenges'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, challenge.name)

    def test_hidden_challenge(self):
        """
        Set challenge visibility to false, and check if it's still shown on the challenges list page.
        """
        client = self.login_client()
        challenge = Challenge.objects.get(name="pwn1")
        challenge.visible = False
        challenge.save()

        response = client.get(reverse('challenge:list-challenges'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, challenge.name)

    def test_submit_correct_flag(self):
        """
        Try to submit correct flag.
        """
        client = self.login_client()
        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': "",
            'end_time': ""
        })

        challenge = Challenge.objects.get(name="pwn1")
        flag = Flag.objects.create(
            challenge=challenge,
            text="ctf{flag_one}"
        )

        response = client.post(reverse('challenge:flag-submit', args=[challenge.pk]), {'challenge_id': challenge.pk, 'flag': flag.text})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The flag is captured!")

    def test_submiting_wrong_flag(self):
        """
        Try to submit wrong flag.
        """
        client = self.login_client()
        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': "",
            'end_time': ""
        })
        challenge = Challenge.objects.get(name="pwn1")
        flag = Flag.objects.create(
            challenge=challenge,
            text="ctf{flag_one}"
        )

        response = client.post(reverse('challenge:flag-submit', args=[challenge.pk]), {'challenge_id': challenge.pk, 'flag': "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "The flag is captured!")
        self.assertContains(response, "Wrong flag!")

    def test_resubmiting_flag(self):
        """
        Try to resubmit flag for already solved task.
        """
        client = self.login_client()
        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': "",
            'end_time': ""
        })
        challenge = Challenge.objects.get(name="pwn1")
        flag = Flag.objects.create(
            challenge=challenge,
            text="ctf{flag_one}"
        )

        response = client.post(reverse('challenge:flag-submit', args=[challenge.pk]), {'challenge_id': challenge.pk, 'flag': flag.text})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The flag is captured!")

        response = client.post(reverse('challenge:flag-submit', args=[challenge.pk]), {'challenge_id': challenge.pk, 'flag': flag.text})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "The flag is captured!")
        self.assertContains(response, "Already solved!")
