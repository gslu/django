# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allows access only to owner users or readonly.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj,"author"):
            owner = obj.author
        elif hasattr(obj,"user"):
            owner = obj.user
        else:
            owner = obj

        return (
            request.method in SAFE_METHODS or
            owner == request.user
            )
