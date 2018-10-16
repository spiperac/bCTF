from django.urls import path

from apps.scoreboard.views import IndexView

app_name = 'scoreboard'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]