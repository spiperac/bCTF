from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # apps
    path('', include('apps.scoreboard.urls')),
    path('challenges/', include('apps.challenges.urls')),

]
