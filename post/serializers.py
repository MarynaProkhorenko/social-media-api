from rest_framework import serializers

from post.models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    model = Post
    fields = (
        "id",
        "created_at",
        "author",
        "content",
        "image",
        "hashtag",
    )
    read_only_fields = ("id", "created_at", "author")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post", "user")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "content", "created_at")
        read_only_fields = ("id", "user", "post", "created_at")


class PostListSerializer(PostSerializer):
    fields = (
        "id",
        "created_at",
        "author",
        "content",
        "image",
        "hashtag",
        "count_likes",
        "count_comments",
    )


class PostDetailSerializer(PostSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "created_at",
            "author",
            "content",
            "image",
            "hashtag",
            "likes",
            "comments",
        )
