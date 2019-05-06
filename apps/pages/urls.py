from django.urls import path
from apps.pages.views import PageCreateView, PageListView, PageView, PageDeleteView, PageUpdateView

app_name = 'pages'
urlpatterns = [
    path('', PageListView.as_view(), name="list-pages"),
    path('create/', PageCreateView.as_view(), name="create-page"),
    path('update/<int:pk>/', PageUpdateView.as_view(), name="update-page"),
    path('delete/<int:pk>/', PageDeleteView.as_view(), name="delete-page"),
    path('page/<slug:slug>/', PageView.as_view(), name="details-page"),
]
