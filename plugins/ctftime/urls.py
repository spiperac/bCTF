from django.urls import path

from plugins.ctftime.views import CTFTimeView

app_name = 'ctftime'
urlpatterns = [
    path('', CTFTimeView.as_view(), name='ctftime'),
]
