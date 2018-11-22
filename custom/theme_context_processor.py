from config.themes import get_theme
from django.conf import settings

def theme_context(request):
    return {
        "theme_static": "{0}{1}/static".format(settings.STATIC_URL, get_theme())
    }