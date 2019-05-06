from django.urls import path

from apps.challenges.views import (AddCategoryView, AttachmentAddView,
                                   AttachmentDeleteView, AttachmentsView,
                                   ChallengesListView, CreateChallengeView,
                                   DeleteCategoryView, DeleteChallengeView,
                                   FlagAddView, FlagDeleteView, FlagsView,
                                   HintAddView, HintDeleteView, HintsView,
                                   SubmitFlagView, ToggleChallengeVisibility,
                                   UpdateCategoryView, UpdateChallengeView)

app_name = 'challenge'
urlpatterns = [
    path('', ChallengesListView.as_view(), name='list-challenges'),
    path('new/', CreateChallengeView.as_view(), name='create-challenge'),
    path('<int:pk>/flag/', SubmitFlagView.as_view(), name='flag-submit'),

    # Category urls
    path('category/add', AddCategoryView.as_view(), name="add-category"),
    path('category/<int:pk>/update', UpdateCategoryView.as_view(), name="update-category"),
    path('category/<int:pk>/delete', DeleteCategoryView.as_view(), name="delete-category"),

    # Challenge urls
    path('togglevisibility', ToggleChallengeVisibility.as_view(), name="toggle-visibility-challenge"),
    path('<int:pk>/update', UpdateChallengeView.as_view(), name="update-challenge"),
    path('<int:pk>/delete', DeleteChallengeView.as_view(), name="delete-challenge"),

    # Flag urls
    path('<int:pk>/flags', FlagsView.as_view(), name="flags"),
    path('<int:pk>/flags/add', FlagAddView.as_view(), name="add-flag"),
    path('flags/delete', FlagDeleteView.as_view(), name="delete-flag"),

    # Hint urls
    path('<int:pk>/hints', HintsView.as_view(), name="hints"),
    path('<int:pk>/hints/add', HintAddView.as_view(), name="add-hint"),
    path('hints/delete', HintDeleteView.as_view(), name="delete-hint"),

    # Attachments urls
    path('<int:pk>/attachments', AttachmentsView.as_view(), name="attachments"),
    path('<int:pk>/attachments/add', AttachmentAddView.as_view(), name="add-attachment"),
    path('attachments/delete', AttachmentDeleteView.as_view(), name="delete-attachment"),

]
