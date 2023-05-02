from django.urls import include, path
from rest_framework import routers

from post.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register("", PostViewSet, basename="post")

urlpatterns = [
    path(
        "<int:post_id>/comments/",
        CommentViewSet.as_view(actions={"get": "list", "post": "create"}),
        name="comment-list",
    ),
    path(
        "<int:post_id>/comments/<int:id>/",
        CommentViewSet.as_view(actions={"get": "retrieve", "delete": "destroy"}),
        name="comment-detail",
    ),
] + path("", include(router.urls))

app_name = "post"
