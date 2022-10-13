from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from equipments.models import User


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return get_object_or_404(
                User,
                telegram_id=request.data.get("telegram_id")
            ).is_staff

    def has_object_permission(self, request, view, obj):
        return get_object_or_404(
                User,
                telegram_id=request.data.get("telegram_id")
            ).is_staff
