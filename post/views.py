from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from post.models import Post, Like
from post.serializers import PostListSerializer, PostDetailSerializer, PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Post.objects.prefetch_related("likes", "comments")
        if self.action in ("retrieve",):
            queryset = queryset.filter(
                Q(author=self.request.user)
                | Q(author__id__in=self.request.user.followings.values("user_id"))
            )

            hashtag = self.request.query_params.get("hashtag")
            if hashtag:
                queryset = queryset.filter(hashtag__icontains=hashtag)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "like":
            return LikeSerializer

        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
        permission_classes=[IsAuthenticated],
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = self.request.user
        serializer = LikeSerializer(data={"post": post.id, "user": user.id})

        if serializer.is_valid():
            serializer.save()
        return_serializer = PostDetailSerializer(self.get_object())
        return Response(return_serializer.errors, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
        permission_classes=[IsAuthenticated],
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = self.request.user
        Like.objects.filter(post_id=post.id, user__id=user.id).delete()

        return_serializer = PostDetailSerializer(self.get_object())
        return Response(return_serializer.errors, status=status.HTTP_200_OK)

