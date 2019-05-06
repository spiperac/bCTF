from django.shortcuts import redirect
from django.urls import reverse

from config import get_key


class InstallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.path.startswith(reverse('installer')):
            return self.get_response(request)

        install_status = get_key("installed")
        if install_status:
            response = self.get_response(request)
            return response
        else:
            return redirect(reverse("installer"))

