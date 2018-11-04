from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import Account


class AccountTests(TestCase):
    def setUp(self):
        self.test_username = "tester"
        self.test_password = "hacker312"
        self.test_email = "tester@testland.com"

    def test_registration(self):
        client = Client()
        request_data = {
            "username": self.test_username,
            "email": self.test_email,
            "password1": self.test_password,
            "password2": self.test_password
        }

        response = client.post(reverse('registration'), request_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Account.objects.filter(username=self.test_username).count() == 1)


    def test_login(self):
        client = Client()
        request_data = {
            "username": self.test_username,
            "password": self.test_password
        }
        account = Account.objects.create(
            username=self.test_username,
            email=self.test_email
        )

        account.set_password(self.test_password)
        account.save()

        response = client.post(reverse('login'), request_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(client.session['_auth_user_id']), account.pk)

        response = client.get(reverse('registration'))
        self.assertEqual(response.status_code, 302)

    def test_profile(self):
        client = Client()
        account = Account.objects.create(
            username=self.test_username,
            email=self.test_email
        )

        account.set_password(self.test_password)
        account.save() 

        login = client.login(username=self.test_username, password=self.test_password)
        self.assertTrue(login)

        response = client.get(reverse('profile', args=[account.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_username)