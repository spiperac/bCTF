from django.urls import path

from apps.teams.views import (CreateTeamView, UpdateTeamView, DetailTeamView,
                              ListTeamView, DeleteTeamView)

app_name = 'teams'
urlpatterns = [
    path('', ListTeamView.as_view(), name='list'),
    path('new/', CreateTeamView.as_view(), name='create'),
    path('<int:pk>/', DetailTeamView.as_view(), name='detail'),
    path('<int:pk>/update', UpdateTeamView.as_view(), name='update'),
    path('<int:pk>/delete', DeleteTeamView.as_view(), name='delete'),
]
