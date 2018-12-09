import os
from django.conf import settings
from config import set_key, get_key


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