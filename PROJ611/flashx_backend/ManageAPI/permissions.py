from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            key = request.META['HTTP_AUTHORIZATION'].split()[1]
            user = Token.objects.get(key=key).user
            # if user.is_superuser:
            #     return True
            # else:
            #     return False
            return user.is_superuser
        except (KeyError, IndexError, Token.DoesNotExist, AuthenticationFailed):
            return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        try:
            key = request.META['HTTP_AUTHORIZATION'].split()[1]
            user = Token.objects.get(key=key).user
            # if user.is_staff:
            #     return True
            # else:
            #     return False
            return user.is_staff
        except (KeyError, IndexError, Token.DoesNotExist, AuthenticationFailed):
            return False
