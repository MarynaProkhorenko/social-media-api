from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user)
