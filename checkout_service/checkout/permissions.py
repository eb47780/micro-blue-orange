from rest_framework import permissions
import requests


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        token = str(request.META['HTTP_AUTHORIZATION'].split()[1])
        response = requests.post('http://127.0.0.1:8001/api/token/verify/', data={"token": token})
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            return False


class IsCheckoutOwnerDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.id

class IsCheckoutItemOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.checkout.customer == request.user.id
