from django.urls import path

from api.views import scores

app_name = 'api'
urlpatterns = [
    path('scores/', scores, name='score'),

]