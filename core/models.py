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
    description = models.TextField(blank=True, help_text=_("Detailed description of the institution"))
    image = models.ImageField(upload_to="institutions/", blank=True, null=True)
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


class JobApplication(models.Model):
    """Job application submitted via the website."""

    STATUS_PENDING = 'PENDING'
    STATUS_REVIEWED = 'REVIEWED'
    STATUS_SHORTLISTED = 'SHORTLISTED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_SHORTLISTED, 'Shortlisted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")

    def __str__(self) -> str:
        return f"{self.full_name} - {self.job.title}"


class CharityApplication(models.Model):
    """Application for charity or financial aid."""

    CATEGORY_PALLIATIVE = 'PALLIATIVE'
    CATEGORY_MARRIAGE = 'MARRIAGE'
    CATEGORY_MEDICAL = 'MEDICAL'
    CATEGORY_EDUCATION = 'EDUCATION'
    CATEGORY_WIDOW = 'WIDOW'
    CATEGORY_OTHER = 'OTHER'

    CATEGORY_CHOICES = [
        (CATEGORY_PALLIATIVE, 'Palliative Care (സാന്ത്വനം)'),
        (CATEGORY_MARRIAGE, 'Marriage Aid (വിവാഹസഹായ നിധി)'),
        (CATEGORY_MEDICAL, 'Medical Aid (ചികിത്സാ സഹായം)'),
        (CATEGORY_EDUCATION, 'Educational Scholarship (സ്കോളർഷിപ്പ്)'),
        (CATEGORY_WIDOW, 'Widow Support (അതിജീവിതം)'),
        (CATEGORY_OTHER, 'Other / General'),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, help_text=_("Contact number for verification."))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text=_("Describe your situation and requirement."))
    document = models.FileField(upload_to='charity_docs/', blank=True, null=True, help_text=_("Upload supporting documents (medical reports, etc.)"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text=_("Internal notes by committee."))

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = _("Charity Application")
        verbose_name_plural = _("Charity Applications")

    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_category_display()}"
