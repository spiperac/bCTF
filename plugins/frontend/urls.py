from django.urls import path

from plugins.frontend.views import FrontendView

app_name = 'frontend'
urlpatterns = [
    path('', FrontendView.as_view(), name='home'),
]

