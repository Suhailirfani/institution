from typing import Iterable

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from .models import User


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for class-based views to restrict by user.role."""

    allowed_roles: Iterable[str] = ()

    def test_func(self) -> bool:
        user: User = self.request.user
        if not user.is_authenticated:
            return False
        if not self.allowed_roles:
            return True
        return user.role in self.allowed_roles or user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("You do not have access to this area.")


class RolePermission(BasePermission):
    """DRF permission class based on user.role."""

    allowed_roles: Iterable[str] = ()

    def has_permission(self, request, view) -> bool:
        user: User = request.user
        if not user or not user.is_authenticated:
            return False
        allowed = getattr(view, "allowed_roles", self.allowed_roles)
        if not allowed:
            return True
        return user.role in allowed or user.is_superuser



