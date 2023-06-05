from django.urls import path

from posts.views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    CommentView,
    PostDeleteView,
    PostUpdateView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="main"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path("<int:pk>/comment/", CommentView.as_view(), name="comment"),
]
