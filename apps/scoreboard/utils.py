import os
from django.conf import settings
from apps.scoreboard.models import Configuration


def get_key(key):
    conf = Configuration.objects.filter(key=key).first()
    if conf:
        return conf.value
    else:
        return None


def set_key(name, value):
    conf = Configuration.objects.get(key=name)
    conf.value = value
    conf.save()


def create_key(key, value):
    Configuration.objects.create(
        key=key,
        value=value
    )


def get_themes():
    themes_path = "{0}/themes/".format(settings.BASE_DIR)
    themes_list = next(os.walk(themes_path))[1]
    for theme in themes_list:
        if theme.startswith("."):
            themes_list.remove(theme)
        if "admin" in theme:
            themes_list.remove(theme)

    return themes_list


def set_theme(theme):
    set_key("theme", theme)


def get_theme():
    theme = get_key("theme")
    if theme:
        return theme
    else:
        return "core"
