import os
from django.urls import path, include

current_dir = os.path.dirname(os.path.abspath(__file__))


def list_plugins():
    """
    returns: List of plugin app names, based on directory name.
    """
    plugin_dirs = next(os.walk(current_dir))[1]
    filtered = [x for x in plugin_dirs if not x.startswith('__')]
    return filtered

def install_plugins():
    """
    INSTALLED_APPS - bCTF original installd apps var
    """
    plugins = []
    for plugin in list_plugins():
        plugins += [
            'plugins.{0}'.format(plugin)
        ]

    return plugins

def install_plugin_urls():
    """
    urlpatterns - bCTF original urlpatterns
    """
    urls = []
    for plugin in list_plugins():
        urls.append(path('{0}/'.format(plugin), include('plugins.{0}.urls'.format(plugin))))

    return urls