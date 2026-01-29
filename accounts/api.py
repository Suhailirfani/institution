from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import RolePermission
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for listing and viewing users (admin/staff only)."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.STAFF]



