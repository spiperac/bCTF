from django import template
from django.conf import settings
from apps.pages.models import Page
from config.config import read_config
register = template.Library()

@register.simple_tag
def config():
    return getattr(settings, "CONFIG_FILE", None)

@register.simple_tag
def get_pages():
    return Page.objects.all()