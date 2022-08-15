from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'moderator':
                return True
        return False


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'user':
                return True
        return False


class IsOwenAdminModeratorOrReadOnly(permissions.BasePermission):
    message = 'Изменить контент может только автор, админ или модератор.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role == 'admin'
            or request.user.is_superuser
            or request.user.role == 'moderator'
            or request.user.role == 'user'
        )
