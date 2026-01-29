from django.conf import settings
from django.db import models


class FinanceReport(models.Model):
    """High-level finance report accessible to committee members."""

    title = models.CharField(max_length=255)
    period_start = models.DateField()
    period_end = models.DateField()
    file = models.FileField(upload_to="committee/finance_reports/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="uploaded_finance_reports",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title


class ProjectStatus(models.Model):
    """Status updates for charity / infrastructure projects."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class MeetingMinute(models.Model):
    """PDF uploads of committee meeting minutes."""

    title = models.CharField(max_length=255)
    meeting_date = models.DateField()
    file = models.FileField(upload_to="committee/meeting_minutes/")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="meeting_minutes_created",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-meeting_date"]

    def __str__(self) -> str:
        return f"{self.meeting_date} - {self.title}"
