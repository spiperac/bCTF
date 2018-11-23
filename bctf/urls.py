from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.accounts.views import RegistrationView, ProfileView, AccountUpdateView, Login
from apps.installer.views import InstallView
from bctf.views import error_view_403, error_view_404, error_view_500
from django.conf.urls import handler403, handler404, handler500
from plugins import list_plugins, install_plugin_urls

handler403 = error_view_403
handler404 = error_view_404
handler500 = error_view_500

urlpatterns = []

# Plugin urls loaded first
urlpatterns += install_plugin_urls()
urlpatterns += [
    # accounts
    path('accounts/login/', Login.as_view(), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password-reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<slug:uidb64>/<slug:token>/)', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/profile/<int:pk>', ProfileView.as_view(), name="profile"),
    path('accounts/settings/', AccountUpdateView.as_view(), name="account-settings"),
    path('registration/', RegistrationView.as_view(), name='registration'),

    # apps
    path('', include('apps.scoreboard.urls')),
    path('api/', include('api.urls')),
    path('administration/', include('apps.administration.urls')),
    # path('teams/', include('apps.teams.urls')),
    path('challenges/', include('apps.challenges.urls')),
    path('pages/', include('apps.pages.urls')),
    path('importer/', include('apps.tasksimporter.urls')),

    # installer
    path('install/', InstallView.as_view(), name='installer'),

]

print(list_plugins())

if settings.DEBUG is True:
    import debug_toolbar
    urlpatterns += [
        path('super-secret/', admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
