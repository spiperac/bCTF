import os
from django.urls import path, include

current_dir = os.path.dirname(os.path.abspath(__file__))


def list_plugins():
    """
    returns: List of plugin app names, based on directory name.
    """
    return next(os.walk(current_dir))[1]

def add_urls(urlpatterns, plugin):
    """
    urlpatterns - bCTF original urlpatterns
    plugin - plugin name to be included in new path
    """
    urlpatterns += path('{0}/'.format(plugin), include('plugins.{0}.urls'.format(plugin)), name=plugin)