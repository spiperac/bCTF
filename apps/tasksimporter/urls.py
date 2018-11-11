from django.urls import path

from apps.tasksimporter.views import ImportTasksView

app_name = 'importer'
urlpatterns = [
    path('', ImportTasksView.as_view(), name='import-tasks'),
]
