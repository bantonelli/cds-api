__author__ = 'brandonantonelli'

from rest_framework import permissions

class IsKitOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.profile


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user