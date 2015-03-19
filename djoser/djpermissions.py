from rest_framework import permissions
from provider.oauth2.models import AccessToken

class IsKitOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.profile


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user.profile
        #elif request.META['Authorization']:
        else:
            auth_header = request.META['Authorization']
            index = auth_header.find('Bearer') + 7
            token_string = auth_header[index:]
            token = AccessToken.objects.get_token(token=token_string)
            user = token.user
            return obj == user.profile


class IsActiveUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            return request.user.is_active
        else:
            auth_header = request.META['Authorization']
            index = auth_header.find('Bearer') + 7
            token_string = auth_header[index:]
            token = AccessToken.objects.get_token(token=token_string)
            user = token.user
            return user.is_active