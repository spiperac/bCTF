from django.http import HttpResponse
from django.shortcuts import render
from ratelimit.exceptions import Ratelimited


def error_view_403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return render(request, template_name=request.template_name ,context={'error': 'test'}, status=429)
    return render(request, 'templates/errors/403.html', status=403)


def error_view_404(request):
    return render(request, 'templates/errors/404.html', status=404)


def error_view_500(request):
    return render(request, 'templates/errors/500.html', status=500)


def rate_limit_hit(request, exception):
    message = "Slow down."
    return HttpResponse(message)
