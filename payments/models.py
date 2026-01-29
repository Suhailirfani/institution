from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from academics.models import StudentProfile


class Payment(models.Model):
    """Represents a fee or donation payment via Razorpay or offline."""

    class Category(models.TextChoices):
        TUITION = "TUITION", _("Tuition Fee")
        EXAM = "EXAM", _("Exam Fee")
        HOSTEL = "HOSTEL", _("Hostel Fee")
        DONATION = "DONATION", _("Donation")

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")
        REFUNDED = "REFUNDED", _("Refunded")

    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="payments",
        blank=True,
        null=True,
        help_text=_("Linked student, if applicable."),
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")

    # Razorpay-specific fields
    razorpay_order_id = models.CharField(max_length=255, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="verified_payments",
        blank=True,
        null=True,
    )
    verified_at = models.DateTimeField(blank=True, null=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_category_display()} - {self.amount} {self.currency} ({self.status})"
