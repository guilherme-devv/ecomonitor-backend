from rest_framework.permissions import BasePermission
from .models import Manager, Monitor


class IsMonitor(BasePermission):
    """
    Allows access only to users with the 'monitor' role.
    """
    def has_permission(self, request, view):
        return request.user.type == Monitor


class IsManager(BasePermission):
    """
    Allows access only to users with the 'manager' role.
    """
    def has_permission(self, request, view):
        return request.user.type == Manager
