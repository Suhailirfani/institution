from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with role-based access.

    Roles are coarse-grained for dashboards; fine-grained permissions
    use Django's built-in permissions and groups.
    """

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STAFF = "STAFF", _("Staff")
        STUDENT = "STUDENT", _("Student")
        PARENT = "PARENT", _("Parent")
        SPONSOR = "SPONSOR", _("Sponsor")
        COMMITTEE = "COMMITTEE", _("Committee Member")
        APPLICANT = "APPLICANT", _("Applicant")

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=Roles.choices,
        default=Roles.STAFF,
    )

    # Basic profile fields useful across roles
    phone = models.CharField(_("phone number"), max_length=20, blank=True)
    is_phone_verified = models.BooleanField(default=False)

    # For soft institutional multi-tenancy / future expansion
    organization_name = models.CharField(
        max_length=255, blank=True, help_text="Institution or branch name (optional)."
    )

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_staff_member(self) -> bool:
        return self.role == self.Roles.STAFF or self.is_staff

    def is_student(self) -> bool:
        return self.role == self.Roles.STUDENT

    def is_parent(self) -> bool:
        return self.role == self.Roles.PARENT

    def is_sponsor(self) -> bool:
        return self.role == self.Roles.SPONSOR

    def is_committee_member(self) -> bool:
        return self.role == self.Roles.COMMITTEE

    def is_applicant(self) -> bool:
        return self.role == self.Roles.APPLICANT

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
