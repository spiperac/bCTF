from django.urls import path

from apps.administration.views import (AccountsView, CTFView,
                                       DeleteAccountView, DockerActionsView,
                                       DockerImageActionsView, DockerLogsView,
                                       DockerView, GeneralUpdateView,
                                       GeneralView, IndexView,
                                       InformationsView, NewListView,
                                       NewsCreateView, NewsDeleteView,
                                       NewsUpdateView, ToggleAccountStateView,
                                       UpdateAccountView)

app_name = 'administration'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('informations/', InformationsView.as_view(), name='informations'),

    # CTF urls
    path('challenges/', CTFView.as_view(), name='challenges'),

    # General urls
    path('general/', GeneralView.as_view(), name='general'),
    path('general/update', GeneralUpdateView.as_view(), name='update-general'),

    # News urls
    path('news/', NewListView.as_view(), name="news"),
    path('news/add', NewsCreateView.as_view(), name="add-news"),
    path('news/<int:pk>/update', NewsUpdateView.as_view(), name="update-news"),
    path('news/<int:pk>/delete', NewsDeleteView.as_view(), name="delete-news"),

    # Account urls
    path('accounts/', AccountsView.as_view(), name='list-accounts'),
    path('accounts/<int:pk>/update',
         UpdateAccountView.as_view(), name="update-account"),
    path('accounts/<int:pk>/delete',
         DeleteAccountView.as_view(), name="delete-account"),
    path('accounts/<int:pk>/toggle',
         ToggleAccountStateView.as_view(), name="toggle-account"),

    # Docker urls
    path('docker/', DockerView.as_view(), name='docker'),
    path('docker/<slug:id>/logs', DockerLogsView.as_view(), name="logs-docker"),
    path('docker/action', DockerActionsView.as_view(), name="action-docker"),
    path('docker/image/action', DockerImageActionsView.as_view(), name="action-image"),


]
