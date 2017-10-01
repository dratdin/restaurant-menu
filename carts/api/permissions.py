from rest_framework.permissions import BasePermission

class CartOwner(BasePermission):
    message = 'You must be the owner of this cart.'

    def has_object_permission(self, request, view, obj):
        return request.session.session_key == obj.session_key
