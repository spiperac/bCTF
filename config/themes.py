from apps.scoreboard.utils import get_theme

def get_theme_url(template):
    full_path = "{0}/{1}".format(get_theme(), template)
    return full_path
