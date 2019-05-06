from django.urls import path

from apps.scoreboard.views import IndexView, ScoreboardView

app_name = 'scoreboard'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
]
