import time
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.six import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from apps.accounts.models import Account
from apps.challenges.models import Challenge, Category, Flag, Hint, Attachment


# "borrowed" from easy_thumbnails/tests/test_processors.py
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class AdministrationTest(TestCase):

    def setUp(self):
        self.admin_account = Account.objects.create_superuser(
            username="administrator",
            email="admin@hackerland.com",
            password="administrator123",
            is_superuser=True
        )
        self.admin_account.set_password("administrator123")
        self.admin_account.save()
        self.test_title = "Example CTF"

    
    def login_as_admin(self):
        """
        Login client as admin user.
        """
        client = Client()

        response = client.post(reverse('login'), {'username': self.admin_account.username, 'password': 'administrator123'})
        self.assertEqual(response.status_code, 302)
        return client
    
    def test_informations_view(self):
        """
        Just load informations menu page.
        """
        client = self.login_as_admin()

        response = client.get(reverse('administration:informations'))
        self.assertEqual(response.status_code, 200)

    def test_ctf_view(self):
        """
        Just load ctf menu page.
        """
        client = self.login_as_admin()

        response = client.get(reverse('administration:ctf'))
        self.assertEqual(response.status_code, 200)

    # def test_docker_view(self):
    #     """
    #     Just load ctf menu page.
    #     """
    #     client = self.login_as_admin()

    #     response = client.get(reverse('administration:docker'))
    #     self.assertEqual(response.status_code, 200)

    def test_toggle_challenge_visibility(self):
        """
        Testing hide/show challenge from administration page.
        """
        client = self.login_as_admin()
        category = Category.objects.create(
            name="pwn"
        )

        challenge = Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000,
            visible=True
        )

        self.assertTrue(Challenge.objects.get(pk=challenge.pk).visible)

        response = client.post(reverse('administration:toggle-visibility-challenge'), {'challenge_id': challenge.pk})
        self.assertFalse(Challenge.objects.get(pk=challenge.pk).visible)

        response = client.post(reverse('administration:toggle-visibility-challenge'), {'challenge_id': challenge.pk})
        self.assertTrue(Challenge.objects.get(pk=challenge.pk).visible)   


    def test_general_change_title(self):
        """
        Test for a title change.
        """
        client = self.login_as_admin()
        new_title = "Example CTF NEW!"
        response = client.post(reverse('administration:update-general'), {'title': new_title})
        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('scoreboard:home'))
        self.assertContains(response, new_title)

    def test_add_delete_flag_view(self):
        """
        Testing flag addition and deletion
        """

        client = self.login_as_admin()
        category = Category.objects.create(
            name="pwn"
        )

        challenge = Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000
        )

        flag = Flag.objects.create(
            challenge=challenge,
            text="ctf{simple_flag}"
        )

        response = client.get(reverse('administration:flags', args=[challenge.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, flag.text)

        response = client.post(reverse('administration:add-flag', args=[challenge.pk, ]), {'challenge_id': challenge.pk, 'flag': 'ctf{second_flag}'})
        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('administration:flags', args=[challenge.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ctf{second_flag}')

        response = client.post(reverse('administration:delete-flag'), {'flag': 2})
        self.assertEqual(response.status_code, 204)        

        response = client.get(reverse('administration:flags', args=[challenge.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'ctf{second_flag}')

    def test_add_delete_hint(self):
        """
        Testing hints addition and deletion.
        """

        client = self.login_as_admin()
        
        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': "",
            'end_time': ""
        })

        category = Category.objects.create(
            name="pwn"
        )

        challenge = Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000
        )   

        hint = Hint.objects.create(
            challenge=challenge,
            text="This is simple hint!"
        )

        response = client.get(reverse('administration:hints', args=[challenge.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, hint.text)    

        response = client.post(reverse('administration:add-hint', args=[challenge.pk, ]), {'challenge_id': challenge.pk, 'hint': 'This is second hint!'})
        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('administration:hints', args=[challenge.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is second hint!')

        response = client.get(reverse('challenge:flag-submit', args=[challenge.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is second hint!')

        hint.delete()

        response = client.get(reverse('challenge:flag-submit', args=[challenge.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is simple hint!")

        response = client.post(reverse('administration:delete-hint'), {'hint': 2})
        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('challenge:flag-submit', args=[challenge.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is second hint!")    


    def test_attachment_add_delete(self):
        """
        Testing attachments with generated image file.
        """
        client = self.login_as_admin()
        category = Category.objects.create(
            name="pwn"
        )

        challenge = Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000
        )   

        # set up form data
        attachment = create_image(None, 'attachment_image.png')
        attachment_file = SimpleUploadedFile('attachment_image.png', attachment.getvalue())
        form_data = {'challenge_id': challenge.pk, 'data': attachment_file}

        response = client.post(reverse('administration:add-attachment', args=[challenge.pk, ]), form_data)
        self.assertEqual(response.status_code, 204)

        attachment_name = Attachment.objects.get(pk=1)

        response = client.get(reverse('administration:attachments', args=[challenge.pk]))
        self.assertContains(response, attachment_name.filename())

        response = client.post(reverse('administration:delete-attachment'), {'attachment': 1})
        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('administration:attachments', args=[challenge.pk]))
        self.assertNotContains(response, attachment_name.filename())

    def test_ctf_time_setup(self):
        """
        Test if timer works just fine.
        """
        client = self.login_as_admin()

        start_time = time.time()
        end_time = time.time() + 20

        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': int(start_time),
            'end_time': int(end_time)
        })

        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('scoreboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,'var startingTime = `None`;')
        self.assertNotContains(response, 'var countDownTime = `None`;')
    
    def test_ctf_time_check_challenges_after_end(self):
        """
        Test if you are able to see challenges after CTF end time pass.
        """
        client = self.login_as_admin()

        category = Category.objects.create(
            name="pwn"
        )

        challenge = Challenge.objects.create(
            category=category,
            name="pwn1",
            description="Test pwn",
            points=1000
        )

        start_time = time.time()
        end_time = time.time() + 5

        response = client.post(reverse('administration:update-general'), {
            'title': self.test_title,
            'start_time': int(start_time),
            'end_time': int(end_time)
        })

        self.assertEqual(response.status_code, 204)

        response = client.get(reverse('scoreboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,'var startingTime = `None`;')
        self.assertNotContains(response, 'var countDownTime = `None`;')
        
        response = client.get(reverse('challenge:list-challenges'))
        self.assertContains(response, challenge.name)
        time.sleep(1)
        response = client.get(reverse('challenge:flag-submit', args=[challenge.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, challenge.description)
        time.sleep(5)

        response = client.get(reverse('challenge:flag-submit', args=[challenge.pk]))
        self.assertEqual(response.status_code, 403)
    

