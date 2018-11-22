from django.shortcuts import render


def error_view_403(request, exception):
    return render(request, 'templates/errors/403.html', status=403)


def error_view_404(request):
    return render(request, 'templates/errors/404.html', status=404)


def error_view_500(request):
    return render(request, 'templates/errors/500.html', status=500)
