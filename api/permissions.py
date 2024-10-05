from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'author'