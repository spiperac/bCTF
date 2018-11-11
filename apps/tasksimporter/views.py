import zipfile
from django.shortcuts import render
from django.views.generic import View
from apps.tasksimporter.forms import ImportTasksForm

class ImportTasksView(View):
    form_class = ImportTasksForm

    def get(self, request, *args, **kwargs):
        return render(self.request, 'tasks/import.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        return render(self.request, 'tasks/import.html', {'form': self.form_class})
