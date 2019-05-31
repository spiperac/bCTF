import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from ratelimit.exceptions import Ratelimited


def error_view_403(request, exception=None):
    if isinstance(exception, Ratelimited):
        messages.error(request, "Slow down.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'templates/errors/403.html', status=403)


def error_view_404(request, exception=None):
    return render(request, 'templates/errors/404.html', status=404)


def error_view_500(request, exception=None):
    return render(request, 'templates/errors/500.html', status=500)


def rate_limit_hit(request, exception):
    message = "Slow down."
    return HttpResponse(message)
