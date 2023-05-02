from typing import Type

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserFollowing
from user.serializers import (
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer, UserListSerializer, FollowingsSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class ManageUserView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self) -> Type[UserRetrieveSerializer | UserUpdateSerializer]:
        if self.action == "retrieve":
            return UserRetrieveSerializer
        return UserUpdateSerializer


class UserView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.prefetch_related("followings", "followers")
        if self.action == "list":
            first_name = self.request.query_params.get("first_name")
            last_name = self.request.query_params.get("last_name")
            country = self.request.query_params.get("country")
            city = self.request.query_params.get("city")

            if first_name:
                queryset = queryset.filter(first_name__icontains=first_name)

            if last_name:
                queryset = queryset.filter(last_name__icontains=last_name)

            if country:
                queryset = queryset.filter(country__icontains=country)

            if city:
                queryset = queryset.filter(city__icontains=city)

        return queryset

    def get_serializer_class(self) -> Type[UserListSerializer | UserRetrieveSerializer]:
        if self.action == "list":
            return UserListSerializer

        return UserRetrieveSerializer


class FollowUnfollowView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowingsSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow",
        url_name="user-follow",
        permission_classes=[IsAuthenticated],
    )
    def follow(self, request, pk=None) -> Response:
        user_id = self.kwargs.get("pk")
        follower_id = self.request.user.id

        if user_id != follower_id:
            data = {"user_id": user_id, "follower_id": follower_id}
            serializer = self.get_serializer(data=data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            read_serializer = UserRetrieveSerializer(self.request.user)
            return Response(read_serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={"message": "User can't follow self"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="unfollow",
        url_name="user-unfollow",
        permission_classes=[IsAuthenticated],
    )
    def unfollow(self, request, pk=None) -> Response:
        user_id = self.kwargs.get("pk")
        follower_id = self.request.user.id
        UserFollowing.objects.filter(user_id=user_id, follower_id=follower_id).delete()
        return Response(status=status.HTTP_200_OK)
