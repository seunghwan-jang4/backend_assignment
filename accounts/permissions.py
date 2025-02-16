from rest_framework import permissions

class IsAuthenticatedUser(permissions.BasePermission):
    """
    인증된 사용자만 접근 가능
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdminUser(permissions.BasePermission):
    """
    관리자만 접근 가능
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # `is_staff=True`인 경우만 접근 가능
