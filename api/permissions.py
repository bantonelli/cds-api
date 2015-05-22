__author__ = 'brandonantonelli'

from rest_framework import permissions
from provider.oauth2.models import AccessToken
from kitbuilder.kitbuilder_v1.models import KitBuilderTemplate

class IsKitOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.profile


class IsTemplateOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        template_id = obj.id
        template = KitBuilderTemplate.objects.get(pk=template_id)
        if request.user:
            user = request.user
            users_templates = user.profile.kitbuilder_templates.all()
            if users_templates.filter(id=template_id).exists():
                return True
            else:
                return False
        #elif request.META['Authorization']:
        else:
            auth_header = request.META.get('Authorization')
            if auth_header is not None:
                index = auth_header.find('Bearer') + 7
                token_string = auth_header[index:]
                token = AccessToken.objects.get_token(token=token_string)
                user = token.user
                users_templates = user.profile.kitbuilder_templates.all()
                if users_templates.filter(id=template_id).exists():
                    return True
                else:
                    return False
            return False


class IsUserProfileOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user.profile
        #elif request.META['Authorization']:
        else:
            auth_header = request.META.get('Authorization')
            if auth_header is not None:
                index = auth_header.find('Bearer') + 7
                token_string = auth_header[index:]
                token = AccessToken.objects.get_token(token=token_string)
                user = token.user
                return obj == user.profile
            return False