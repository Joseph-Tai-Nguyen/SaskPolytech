from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        key = request.META['HTTP_AUTHORIZATION'].split()[1]
        user = Token.objects.get(key=key).user
        if user.is_superuser:
            return True
        else:
            return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        key = request.META['HTTP_AUTHORIZATION'].split()[1]
        user = Token.objects.get(key=key).user
        if user.is_staff:
            return True
        else:
            return False
