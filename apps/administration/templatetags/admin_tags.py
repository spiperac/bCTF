from django import template
from apps.administration.utils import check_docker

register = template.Library()


@register.simple_tag
def docker_exists():
    return check_docker()
