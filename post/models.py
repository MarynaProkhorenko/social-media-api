import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/post_images/", filename)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=post_image_file_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post {self.id} by {self.author}"


