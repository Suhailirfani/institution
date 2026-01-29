from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AcademicYear, Institution


class Programme(models.Model):
    """Represents a course / class into which admissions are made."""

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="programmes",
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("institution", "code")
        verbose_name = _("Programme")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class AdmissionApplication(models.Model):
    """Online admission application with basic KYC and document upload."""

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", _("Submitted")
        UNDER_REVIEW = "UNDER_REVIEW", _("Under Review")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="admission_applications",
    )
    programme = models.ForeignKey(
        Programme,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    # Applicant basic info (no login required for MVP)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    guardian_name = models.CharField(max_length=255, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_applications",
        blank=True,
        null=True,
    )
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.programme} ({self.academic_year})"


class AdmissionDocument(models.Model):
    """Uploaded documents for an application (certificates, ID proof, etc.)."""

    application = models.ForeignKey(
        AdmissionApplication,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="admissions/documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} for {self.application}"
