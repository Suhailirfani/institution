from django.conf import settings
from django.db import models

from academics.models import StudentProfile
from core.models import AcademicYear


class SponsorProfile(models.Model):
    """Profile for sponsors who support students financially."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sponsor_profile",
    )
    organization_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username


class SponsorshipAllocation(models.Model):
    """Link between a sponsor and a sponsored student."""

    sponsor = models.ForeignKey(
        SponsorProfile,
        on_delete=models.CASCADE,
        related_name="allocations",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="sponsorships",
    )
    start_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="sponsorships_started",
    )
    end_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="sponsorships_ended",
        blank=True,
        null=True,
    )
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("sponsor", "student", "start_year")

    def __str__(self) -> str:
        return f"{self.sponsor} -> {self.student} ({self.start_year})"
