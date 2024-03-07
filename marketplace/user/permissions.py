from rest_framework.permissions import BasePermission
from .models import UserRoles

class IsModer(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR or request.user.is_superuser