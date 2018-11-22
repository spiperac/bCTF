from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri
from urllib.parse import urljoin

from apps.scoreboard.utils import get_theme


class ThemeStorage(FileSystemStorage):

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip('/')
        return urljoin(self.base_url, "{0}/static/{1}".format(get_theme(), url))