from django.urls import path

from apps.administration.views import IndexView, InformationsView, CTFView, AddChallengeView, UpdateChallengeView, DeleteChallengeView, \
                                         AddCategoryView, UpdateCategoryView, DeleteCategoryView, FlagsView, FlagAddView, HintsView, HintAddView

app_name = 'administration'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('informations/', InformationsView.as_view(), name='informations'),
    
    # CTF urls
    path('ctf/', CTFView.as_view(), name='ctf'),

    # Category urls
    path('ctf/category/add', AddCategoryView.as_view(), name="add-category"),
    path('ctf/category/<int:pk>/update', UpdateCategoryView.as_view(), name="update-category"),
    path('ctf/category/<int:pk>/delete', DeleteCategoryView.as_view(), name="delete-category"),

    # Challenge urls
    path('ctf/challenge/add', AddChallengeView.as_view(), name="add-challenge"),
    path('ctf/challenge/<int:pk>/update', UpdateChallengeView.as_view(), name="update-challenge"),
    path('ctf/challenge/<int:pk>/delete', DeleteChallengeView.as_view(), name="delete-challenge"),

    # Flag urls
    path('ctf/challenge/<int:pk>/flags', FlagsView.as_view(), name="flags"),
    path('ctf/challenge/<int:pk>/flags/add', FlagAddView.as_view(), name="add-flag"),

    # Hint urls
    path('ctf/challenge/<int:pk>/hints', HintsView.as_view(), name="hints"),
    path('ctf/challenge/<int:pk>/hints/add', HintAddView.as_view(), name="add-hint"),

]