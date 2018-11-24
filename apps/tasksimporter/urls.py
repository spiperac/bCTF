from django.urls import path

from apps.tasksimporter.views import ImportTasksView, ExportTasksView

app_name = 'importer'
urlpatterns = [
    path('', ImportTasksView.as_view(), name='import-tasks'),
    path('export/', ExportTasksView.as_view(), name='export')
]
