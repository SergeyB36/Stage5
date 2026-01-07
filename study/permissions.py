from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name="Moderator").exists()


class IsOwnerOrIsModerator(BasePermission):
    def has_permission(self, request, view):
        user = self.request.user
        return user.is_authenticated and (user == view.get_object().owner or user.groups.filter(name="Moderator").exists())

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().owner

class CanCreatePermission(BasePermission):
    def has_permission(self, request, view):
        user = self.request.user
        return user.is_authenticated and not user.groups.filter(name="Moderator").exists()
