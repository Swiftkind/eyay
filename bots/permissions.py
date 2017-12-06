from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    message = 'You must an admin or the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.creator
        