from django.urls import path

from api.views import scores, top_scores

app_name = 'api'
urlpatterns = [
    path('scores/', scores, name='score'),
    path('top/', top_scores, name='top'),

]