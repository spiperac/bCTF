from apps.scoreboard.models import Configuration
from django.core.cache import cache


def get_key(key):
    conf = cache.get(key)
    if conf is not None:
        return conf
    else:
        conf = Configuration.objects.filter(key=key).first()
        if conf:
            cache.set(key, conf.value)
            return conf.value
        else:
            return None


def set_key(name, value):
    conf = Configuration.objects.get(key=name)
    conf.value = value
    conf.save()

    cache.set(name, value)


def create_key(key, value):
    Configuration.objects.create(
        key=key,
        value=value
    )
    cache.set(key, value)