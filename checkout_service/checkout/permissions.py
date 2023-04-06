from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class IsCheckoutOwnerDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.id


class IsCheckoutOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj.customer == request.user.id


class IsCheckoutItemOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.checkout.customer == request.user.id
