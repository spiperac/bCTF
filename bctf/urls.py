from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.accounts.views import RegistrationView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/profile/<int:pk>', ProfileView.as_view(), name="profile"),
    path('registration/', RegistrationView.as_view(), name='registration'),

    # apps
    path('', include('apps.scoreboard.urls')),
    path('api/', include('api.urls')),
    path('challenges/', include('apps.challenges.urls')),

]
