from hashlib import md5
from django import template

register = template.Library()


@register.filter(name='get_avatar')
def get_avatar(user, size=35):
    if user.avatar is None:
        email = str(user.email.strip().lower()).encode('utf-8')
        email_hash = md5(email).hexdigest()
        url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
        return url.format(email_hash, size)
    else:
        return user.avatar.url
