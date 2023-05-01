from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from user.views import CreateUserView, ManageUserView, UserView, FollowUnfollowView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "me/",
        ManageUserView.as_view(
            actions={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="manage"
    ),
    path("", UserView.as_view(actions={"get": "list"}), name="user-list"),
    path("<int:pk>/", UserView.as_view(actions={"get": "retrieve",}), name="user-detail"),
    path(
        "<int:pk>/follow/",
        FollowUnfollowView.as_view(actions={"post": "follow"}),
        name="user-follow",
    ),
    path(
        "<int:pk>/unfollow/",
        FollowUnfollowView.as_view(actions={"post": "unfollow"}),
        name="user-unfollow",
    ),
]

app_name = "user"
