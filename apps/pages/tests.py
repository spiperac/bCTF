from django.test import TestCase, Client
from django.urls import reverse
from apps.pages.models import Page
from apps.accounts.models import Account


class PagesTest(TestCase):

    def setUp(self):
        pass

    def login_as_admin(self):
        client = Client()
        admin_account = Account.objects.create_superuser(
            username="administrator",
            email="admin@hackerland.com",
            password="administrator123",
            is_superuser=True
        )
        admin_account.set_password("administrator123")
        admin_account.save()
        response = client.post(reverse('login'), {'username': admin_account.username, 'password': 'administrator123'})
        self.assertEqual(response.status_code, 302)
        return client

    def test_create_page(self):
        """
        Test page creation and listing.
        """
        client = self.login_as_admin()
        page = Page.objects.create(
            title="Page1",
            slug="page1",
            content="""
            This is example test page.
            Content of this page should be clearly visible when you visit slug href.
            """
        )

        response = client.get(reverse('pages:list-pages'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, page.title)

        response = client.get(reverse('pages:details-page', args=[page.slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is example test page.")

    def test_delete_page(self):
        """
        Test page deletion.
        """
        client = self.login_as_admin()
        page = Page.objects.create(
            title="Page1",
            slug="page1",
            content="""
            This is example test page.
            Content of this page should be clearly visible when you visit slug href.
            """
        )

        response = client.get(reverse('pages:list-pages'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, page.title)

        # use get instead of post
        response = client.get(reverse('pages:delete-page', args=[page.pk, ]), {'page': page})
        self.assertEqual(response.status_code, 302)

        response = client.get(reverse('pages:list-pages'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, page.title)
