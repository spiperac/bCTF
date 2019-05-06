from hashlib import md5
from django import template

register = template.Library()


@register.filter(name='get_avatar')
def get_avatar(user, size=35):
    if not user.avatar:
        email = str(user.email.strip().lower()).encode('utf-8')
        email_hash = md5(email).hexdigest()
        url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
        return url.format(email_hash, size)
    else:
        return user.avatar.url


@register.filter(name="to_word")
def int_to_en(num):
    value = str(num)
    if len(value) > 1:
        secondToLastDigit = value[-2]
        if secondToLastDigit == '1':
            return '{0}th'.format(value)
    lastDigit = value[-1]
    if (lastDigit == '1'):
        return '{0}st'.format(value)
    elif (lastDigit == '2'):
        return '{0}nd'.format(value)
    elif (lastDigit == '3'):
        return '{0}rd'.format(value)
    else:
        return '{0}th'.format(value)
