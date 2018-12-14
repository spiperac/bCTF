from django import template
from config import get_key
from apps.pages.models import Page
register = template.Library()


@register.simple_tag
def config(key):
    return get_key(key)


@register.simple_tag
def get_pages():
    return Page.objects.all()
