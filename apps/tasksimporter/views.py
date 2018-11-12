import zipfile
import os
import json
import yaml
from django.shortcuts import render
from django.conf import settings
from django.views.generic import View
from apps.tasksimporter.forms import ImportTasksForm
from django.core.files.storage import FileSystemStorage
from apps.tasksimporter.utils import parse_tasks_yaml


class ImportTasksView(View):
    form_class = ImportTasksForm

    def get(self, request, *args, **kwargs):
        return render(self.request, 'tasks/import.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = ImportTasksForm(request.POST, request.FILES)
        if form.is_valid():
            # Handling file upload
            post_file = request.FILES['zip_file']
            fs = FileSystemStorage(location=settings.ZIP_STORAGE_ROOT)
            filename = fs.save("{0}/{1}".format(settings.ZIP_STORAGE_ROOT, post_file.name), post_file)
            uploaded_file_url = fs.url(filename)

            # Unziping file
            directory_extract = "{0}/{1}".format(settings.ZIP_STORAGE_ROOT, "tasks")
            zip_ref = zipfile.ZipFile(filename, 'r')
            zip_ref.extractall(directory_extract)
            zip_ref.close()

            # Read tasks file
            tasks_base_dir = "{0}/{1}".format(directory_extract, str(post_file)[:-4])
            tasks_file_path = "{0}/{1}".format(tasks_base_dir, "tasks.yml")

            if os.path.isfile(tasks_file_path):
                with open(tasks_file_path, 'r') as tasks_file:
                    tasks_data_yaml = yaml.load(tasks_file)

                # Parsing tasks
                tasks = parse_tasks_yaml(base_path=tasks_base_dir, yaml_data=tasks_data_yaml)
                for task in tasks:
                    task.create()

            else:
                print("File does not exist!")

            return render(self.request, 'tasks/import.html', {'form': self.form_class})
