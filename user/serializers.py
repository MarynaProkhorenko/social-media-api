from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserFollowing


class FollowingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = (
            "user_id",
            "follower_id"
        )


class UserFollowSerializer(serializers.ModelSerializer):
    following = serializers.CharField(
        read_only=True,
        source="user_id"
    )

    class Meta:
        model = UserFollowing
        fields = (
            "user_id",
            "following",
        )


class UserFollowersSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(
        read_only=True,
        source="follower_id"
    )

    class Meta:
        model = UserFollowing
        fields = (
            "follower_id",
            "follower",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
            "country",
            "city",
            "picture",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    followings = UserFollowSerializer(read_only=True, many=True)
    followers = UserFollowersSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
            "country",
            "city",
            "picture",
            "followings",
            "followers",
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id",
                  "first_name",
                  "last_name",
                  "country",
                  "city",
                  "picture",
                  "count_followers",
                  )
