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


class IsOwner(permissions.BasePermission):
    message = 'Изменить контент может только автор, админ или модератор.'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Изменить контент может только админ.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'
