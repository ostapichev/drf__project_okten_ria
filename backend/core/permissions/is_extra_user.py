from rest_framework.permissions import BasePermission

from core.dataclasses.user_dataclasses import UserDataClass


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_superuser)


class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_premium)


class IsAdminOrWriteOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user: UserDataClass = request.user
        return bool(request.user and request.user.is_staff and request.user.is_manager)
