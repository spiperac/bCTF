from django.urls import path

from apps.administration.views import IndexView, InformationsView, CTFView, AddChallengeView, UpdateChallengeView, DeleteChallengeView, \
                                         AddCategoryView, UpdateCategoryView, DeleteCategoryView, FlagsView, FlagAddView, HintsView, \
                                         HintAddView, HintDeleteView, FlagDeleteView, AttachmentsView, AttachmentAddView, AttachmentDeleteView, \
                                         AccountsView, UpdateAccountView, DeleteAccountView, ToggleAccountStateView, ToggleChallengeVisibility, \
                                         DockerView, DockerLogsView, DockerActionsView, DockerImageActionsView, GeneralView, GeneralUpdateView

app_name = 'administration'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('informations/', InformationsView.as_view(), name='informations'),
    
    # CTF urls
    path('ctf/', CTFView.as_view(), name='ctf'),

    # General urls
    path('general/', GeneralView.as_view(), name='general'),
    path('general/update', GeneralUpdateView.as_view(), name='update-general'),

    # Category urls
    path('ctf/category/add', AddCategoryView.as_view(), name="add-category"),
    path('ctf/category/<int:pk>/update', UpdateCategoryView.as_view(), name="update-category"),
    path('ctf/category/<int:pk>/delete', DeleteCategoryView.as_view(), name="delete-category"),

    # Challenge urls
    path('ctf/challenge/add', AddChallengeView.as_view(), name="add-challenge"),
    path('ctf/challenge/togglevisibility', ToggleChallengeVisibility.as_view(), name="toggle-visibility-challenge"),
    path('ctf/challenge/<int:pk>/update', UpdateChallengeView.as_view(), name="update-challenge"),
    path('ctf/challenge/<int:pk>/delete', DeleteChallengeView.as_view(), name="delete-challenge"),

    # Flag urls
    path('ctf/challenge/<int:pk>/flags', FlagsView.as_view(), name="flags"),
    path('ctf/challenge/<int:pk>/flags/add', FlagAddView.as_view(), name="add-flag"),
    path('ctf/flags/delete', FlagDeleteView.as_view(), name="delete-flag"),

    # Hint urls
    path('ctf/challenge/<int:pk>/hints', HintsView.as_view(), name="hints"),
    path('ctf/challenge/<int:pk>/hints/add', HintAddView.as_view(), name="add-hint"),
    path('ctf/hints/delete', HintDeleteView.as_view(), name="delete-hint"),

    # Hint urls
    path('ctf/challenge/<int:pk>/attachments', AttachmentsView.as_view(), name="attachments"),
    path('ctf/challenge/<int:pk>/attachments/add', AttachmentAddView.as_view(), name="add-attachment"),
    path('ctf/attachments/delete', AttachmentDeleteView.as_view(), name="delete-attachment"),

    # Account urls
    path('accounts/', AccountsView.as_view(), name='list-accounts'),
    path('accounts/<int:pk>/update', UpdateAccountView.as_view(), name="update-account"),
    path('accounts/<int:pk>/delete', DeleteAccountView.as_view(), name="delete-account"),
    path('accounts/<int:pk>/toggle', ToggleAccountStateView.as_view(), name="toggle-account"),

    # Docker urls
    path('docker/', DockerView.as_view(), name='docker'),
    path('docker/<slug:id>/logs', DockerLogsView.as_view(), name="logs-docker"),
    path('docker/action', DockerActionsView.as_view(), name="action-docker"),
    path('docker/image/action', DockerImageActionsView.as_view(), name="action-image"),


]