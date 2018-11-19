from django import template
from apps.scoreboard.utils import get_key, get_theme
from apps.pages.models import Page
register = template.Library()


@register.simple_tag
def config(key):
    return get_key(key)


@register.simple_tag
def get_pages():
    return Page.objects.all()

@register.simple_tag
def get_theme_template():
    return get_theme()