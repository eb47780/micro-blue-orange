from rest_framework import permissions


class IsClientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class IsAddressOwnerDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer_id == request.user.id
