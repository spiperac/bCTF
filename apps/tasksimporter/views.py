import zipfile
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from apps.tasksimporter.forms import ImportTasksForm
from django.core.files.storage import FileSystemStorage
from apps.tasksimporter.utils import feed_tasks, clean_base_path, export_as_zip


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ImportTasksView(UserIsAdminMixin, View):
    form_class = ImportTasksForm

    def get(self, request, *args, **kwargs):
        return render(self.request, 'templates/tasks/import.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = ImportTasksForm(request.POST, request.FILES)
        if form.is_valid():
            # Handling file upload
            post_file = request.FILES['zip_file']
            fs = FileSystemStorage(location=settings.ZIP_STORAGE_ROOT)
            filename = fs.save("{0}/{1}".format(settings.ZIP_STORAGE_ROOT, post_file.name), post_file)
            fs.url(filename)

            # Unziping file
            directory_extract = "{0}/{1}".format(settings.ZIP_STORAGE_ROOT, "tasks")
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall(directory_extract)
            zip_ref.close()

            # Parsing tasks
            tasks_base_dir = "{0}/{1}".format(directory_extract, str(post_file)[:-4])
            import_log = []
            tasks = feed_tasks(base_path=tasks_base_dir)
            for task in tasks:
                try:
                    task.create()
                    import_log.append(task.log)
                except Exception as exc:
                    task.log.append('Error: Improting of {0} failed because of: {1}'.format(task.name, exc))
                    import_log.append(task.log)

            clean_base_path(tasks_base_dir)

            return render(self.request, 'templates/tasks/import.html', {'form': self.form_class, 'import_log': import_log})


class ExportTasksView(UserIsAdminMixin, View):
    def get(self, request, *args, **kwargs):
        archive = export_as_zip()
        zip_name = "tasks-{0}".format(datetime.now())
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename={0}.zip".format(zip_name)

        archive.seek(0)
        response.write(archive.read())
        
        return response
