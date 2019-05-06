from django.urls import path

from api.views import scores, top_scores, events, teams

app_name = 'api'
urlpatterns = [
    path('scores/', scores, name='score'),
    path('top/', top_scores, name='top'),
    path('events/', events, name='events'),
    path('teams/', teams, name='teams'),
]