from django.core.exceptions import SuspiciousFileOperation
from django.template import Origin, TemplateDoesNotExist
from django.utils._os import safe_join
from django.template.loaders.base import Loader
from config.themes import get_theme


class AdminTemplateLoader(Loader):

    def __init__(self, engine, dirs=None):
        super().__init__(engine)
        self.dirs = dirs

    def get_dirs(self):
        return self.dirs if self.dirs is not None else self.engine.dirs

    def get_contents(self, origin):
        try:
            with open(origin.name, encoding=self.engine.file_charset) as fp:
                return fp.read()
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)

    def get_template_sources(self, template_name):
        """
        Return an Origin object pointing to an absolute path in each directory
        in template_dirs. For security reasons, if a path doesn't lie inside
        one of the template_dirs it is excluded from the result set.
        """
        template_name = "admin/{1}".format(get_theme(), template_name)

        for template_dir in self.get_dirs():
            try:
                name = safe_join(template_dir, template_name)
            except SuspiciousFileOperation:
                # The joined path was located outside of this template_dir
                # (it might be inside another one, so this isn't fatal).
                continue

            yield Origin(
                name=name,
                template_name=template_name,
                loader=self,
            )
