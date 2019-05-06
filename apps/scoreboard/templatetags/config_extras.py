from django import template
from config import get_key
from apps.pages.models import Page
from django.core.cache import cache
register = template.Library()


@register.simple_tag
def config(key):
    return get_key(key)


@register.simple_tag
def get_pages():
    pages = cache.get('pages')
    if pages is None:
        obj = Page.objects.all()
        cache.set('pages', obj)
        return obj
    else:
        return pages