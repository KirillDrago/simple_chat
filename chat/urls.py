from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    ThreadCreateView,
    ThreadDeleteView,
    MessageListCreateView,
    UserListView,
    ThreadListView,
    ThreadRetrieveView,
)

urlpatterns = [
    path("threads/", ThreadListView.as_view(), name="thread-list"),
    path("threads/create/", ThreadCreateView.as_view(), name="thread-create"),
    path(
        "threads/<int:pk>/",
        ThreadRetrieveView.as_view(),
        name="thread-retrieve",
    ),
    path(
        "threads/<int:pk>/delete/",
        ThreadDeleteView.as_view(),
        name="thread-delete",
    ),
    path(
        "threads/<int:pk>/send_message/",
        MessageListCreateView.as_view(),
        name="message-create",
    ),
    path("users/", UserListView.as_view(), name="users-list"),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "chat"
