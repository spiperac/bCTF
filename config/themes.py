import os
from django.conf import settings
from config import set_key, get_key
from django.core.cache import cache


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
    cache.set("theme", theme)


def get_theme():
    theme = cache.get("theme")
    if theme is not None:
        print("cached theme")
        return theme
    else:
        theme = get_key("theme")
        if theme:
            cache.set("theme", theme)
            return theme
        else:
            cache.set("theme", "core")
            return "core"
