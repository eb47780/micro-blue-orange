from rest_framework import permissions

# Check is object id to request id
class IsClientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
  
 # Check if address owner id to request id 
class IsAddressOwnerDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer_id == request.user.id