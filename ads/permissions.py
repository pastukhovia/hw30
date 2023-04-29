from rest_framework import permissions

from users.models import User


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.ADMIN or request.user.role == User.MODERATOR:
            return True
        return False
