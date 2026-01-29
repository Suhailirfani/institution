from django.db import models
from django.utils.translation import gettext_lazy as _


class AcademicYear(models.Model):
    """Shared academic year model used across admissions and academics."""

    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=_("Display label, e.g. 2025-26"),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return self.name


class Institution(models.Model):
    """Represents an institution or campus under the society."""

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")

    def __str__(self) -> str:
        return self.name


class CMSPage(models.Model):
    """Simple admin-manageable content pages for the public website."""

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self) -> str:
        return self.title


class NotificationLog(models.Model):
    """Stores sent notifications for audit and transparency."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    CHANNEL_CHOICES = [
        (EMAIL, "Email"),
        (SMS, "SMS"),
    ]

    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    to = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.channel} to {self.to} at {self.created_at:%Y-%m-%d %H:%M}"


class NewsItem(models.Model):
    """News and updates for the ticker and home page."""

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, help_text=_("Show in news ticker/highlights."))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class JobOpening(models.Model):
    """Job vacancies for the Career page."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    application_link = models.URLField(blank=True, help_text=_("External link or mailto: syntax."))
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_at"]
        verbose_name = _("Job Opening")
        verbose_name_plural = _("Job Openings")

    def __str__(self) -> str:
        return self.title
