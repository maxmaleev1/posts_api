from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSelfOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff
        return request.user.is_staff or obj == request.user


class IsAdminOrAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or obj.author == request.user
