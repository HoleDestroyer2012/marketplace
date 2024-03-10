from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import UserRoles

class IsModer(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR or request.user.is_superuser


class NotBanned(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_banned:
            raise PermissionDenied('You are banned')
        return True