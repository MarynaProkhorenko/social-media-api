from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from post.permissions import IsAuthor
from post.models import Post, Like, Comment
from post.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostSerializer,
    LikeSerializer,
    CommentSerializer
)


class PostViewSet(viewsets.ModelViewSet):

    def get_queryset(self) -> QuerySet:
        queryset = Post.objects.prefetch_related("likes", "comments")
        if self.action in ("retrieve", "like", "unlike"):
            queryset = queryset.filter(
                Q(author=self.request.user)
                | Q(author__id__in=self.request.user.followings.values("user_id"))
            )

            hashtag = self.request.query_params.get("hashtag")
            if hashtag:
                queryset = queryset.filter(hashtag__icontains=hashtag)

        return queryset

    def get_serializer_class(self) -> PostSerializer:
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "like":
            return LikeSerializer

        return PostSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthor()]
        return [IsAuthenticated()]

    @extend_schema(
        methods=["POST"], request=None, responses={200: PostDetailSerializer}
    )
    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
        permission_classes=[IsAuthenticated],
    )
    def like(self, request, pk=None) -> Response:
        """Endpoint for post like. Returns the post detail"""
        post = self.get_object()
        user = self.request.user
        serializer = LikeSerializer(data={"post": post.id, "user": user.id})

        if serializer.is_valid():
            serializer.save()
        return_serializer = PostDetailSerializer(self.get_object())
        return Response(return_serializer.errors, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["POST"], request=None, responses={200: PostDetailSerializer}
    )
    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
        permission_classes=[IsAuthenticated],
    )
    def unlike(self, request, pk=None) -> Response:
        """Endpoint for post unlike. Returns the post detail"""
        post = self.get_object()
        user = self.request.user
        Like.objects.filter(post_id=post.id, user__id=user.id).delete()

        return_serializer = PostDetailSerializer(self.get_object())
        return Response(return_serializer.errors, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=str,
                description="Filter posts by hashtag",
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> QuerySet:
        return super().list(request, *args, **kwargs)


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CommentSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self) -> QuerySet:
        return Comment.objects.select_related("author", "post").filter(
            Q(post__author=self.request.user)
            | Q(post__author_id__in=self.request.user.followings.values("user_id"))
        )

    def get_permissions(self) -> list[BasePermission]:
        if self.action == "destroy":
            return [IsAuthor()]
        return [IsAuthenticated()]
