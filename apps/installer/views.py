from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from config import config
from apps.accounts.models import Account
from apps.installer.forms import InstallForm


class UserIsAnonymousMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_anonymous


class InstallView(UserIsAnonymousMixin, View):
    form_class = InstallForm

    def get(self, request, *args, **kwargs):
        if Account.objects.count() == 0:
            return render(self.request, 'installer/install.html', {'form': self.form_class})
        else:
            return redirect('scoreboard:home')

    def post(self, request, *args, **kwargs):
        if Account.objects.count() == 0:
            form = InstallForm(request.POST)
            if form.is_valid():
                new_admin = Account(
                    username=request.POST['admin_username'],
                    email=request.POST['admin_email'],
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
                new_admin.set_password(request.POST['admin_password'])
                new_admin.save()

                config.clear_config()
                configuration = config.read_config()
                configuration['ctf']['title'] = request.POST['ctf_name']
                config.update_config(configuration)
                config.reload_settings()

                new_admin.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, new_admin)
                return render(self.request, 'installer/success.html')
        else:
            return HttpResponse(status=403)
