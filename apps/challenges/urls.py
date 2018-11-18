from django.urls import path

from apps.challenges.views import ChallengesListView, SubmitFlagView, CreateChallengeView

app_name = 'challenge'
urlpatterns = [
    path('', ChallengesListView.as_view(), name='list-challenges'),
    path('new/', CreateChallengeView.as_view(), name='create-challenge'),
    path('<int:pk>/flag/', SubmitFlagView.as_view(), name='flag-submit'),
]
